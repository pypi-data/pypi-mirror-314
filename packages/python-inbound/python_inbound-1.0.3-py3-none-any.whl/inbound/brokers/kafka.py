import asyncio
from functools import partial
from urllib.parse import urlparse

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer, TopicPartition
from aiokafka.admin import AIOKafkaAdminClient, NewTopic

from inbound.brokers.base import Broker
from inbound.envelope import Envelope
from inbound.event import Event
from inbound.serializers import JSONSerializer, Serializer
from inbound.utils import cancel_task


class KafkaBroker(Broker):
    """
    A Kafka Broker using `aiokafka` as the underlying library.
    """

    backend = "kafka"

    _producer: AIOKafkaProducer | None = None
    _admin: AIOKafkaAdminClient | None = None
    _consumers: dict[str, AIOKafkaConsumer] = {}
    _consumer_tasks: dict[str, asyncio.Task] = {}
    _inbound_queue: asyncio.Queue[tuple[str, Envelope]]

    def __init__(
        self,
        url: str,
        serializer: type[Serializer] = JSONSerializer,
        node_id: str | None = None,
        *args,
        consumer_tag: str | None = None,
        autocreate_topics: bool = True,
        topic_replication_factor: int = 1,
        topic_partitions: int = 1,
        **kwargs,
    ) -> None:
        super().__init__(url, serializer, node_id, *args, **kwargs)
        self._kwargs = kwargs

        self._netloc = urlparse(url).netloc
        self._consumer_tag = consumer_tag or "inbound"
        self._autocreate_topics = autocreate_topics
        self._topic_replication_factor = topic_replication_factor
        self._topic_partitions = topic_partitions
        self._existing_topics: list[str] = []
        self._lock = asyncio.Lock()

    async def connect(self) -> None:
        if not self._producer:
            self._producer = AIOKafkaProducer(
                bootstrap_servers=self._netloc,
                client_id=self.node_id,
                **self._kwargs,
            )
            await self._producer.start()

        if not self._admin:
            self._admin = AIOKafkaAdminClient(
                bootstrap_servers=self._netloc,
                client_id=self.node_id,
            )
            await self._admin.start()
            self._existing_topics = await self._admin.list_topics()

        self._inbound_queue = asyncio.Queue()

    async def disconnect(self) -> None:
        if self._consumers:
            for consumer in self._consumers.values():
                await consumer.stop()

        if self._producer:
            await self._producer.stop()

        if self._admin:
            self._admin = None

        if self._consumer_tasks:
            for task in self._consumer_tasks.values():
                await cancel_task(task)

    async def subscribe(self, channel: str) -> None:
        async with self._lock:
            if channel not in self._consumers:
                if self._autocreate_topics and self._admin and channel not in self._existing_topics:
                    await self._admin.create_topics(
                        [
                            NewTopic(
                                name=channel,
                                num_partitions=self._topic_partitions,
                                replication_factor=self._topic_replication_factor,
                            )
                        ]
                    )
                    self._existing_topics.append(channel)

                consumer = AIOKafkaConsumer(
                    channel,
                    bootstrap_servers=self._netloc,
                    group_id=self._consumer_tag,
                    client_id=self.node_id,
                    enable_auto_commit=False,
                )
                await consumer.start()

                self._consumers[channel] = consumer
                self._consumer_tasks[channel] = asyncio.create_task(self._consume_channel(consumer))

    async def unsubscribe(self, channel: str) -> None:
        async with self._lock:
            if channel in self._consumers:
                consumer = self._consumers.pop(channel)
                await consumer.stop()

                task = self._consumer_tasks.pop(channel)
                await cancel_task(task)

    async def publish(self, channel: str, event: Event, **kwargs) -> None:
        assert self._producer is not None, "Producer is not connected"

        headers = event.headers or {}
        headers["x-event-type"] = event.type

        await self._producer.send_and_wait(
            topic=channel,
            key=None,
            value=self.serializer.serialize(event.data),
            headers=[(str(k), str(v).encode()) for k, v in headers.items()],
            **kwargs,
        )

    async def next(self) -> tuple[str, Envelope]:
        return await self._inbound_queue.get()

    async def _consume_channel(self, consumer: AIOKafkaConsumer) -> None:
        async for message in consumer:
            try:
                headers = {k: v.decode() for k, v in message.headers}
                event = Event(
                    type=headers.pop("x-event-type", "unknown"),
                    headers=headers,
                    data=self.serializer.deserialize(message.value),
                )
                topic_partition = TopicPartition(
                    message.topic,
                    message.partition,
                )

                await self._inbound_queue.put(
                    (
                        message.topic,
                        Envelope(
                            event,
                            ack=partial(
                                self._ack,
                                consumer=consumer,
                                topic_partition=topic_partition,
                                offset=message.offset,
                            ),
                            nack=partial(
                                self._nack,
                                consumer=consumer,
                                topic_partition=topic_partition,
                                offset=message.offset,
                            ),
                        ),
                    )
                )
            except Exception:
                continue

        await consumer.stop()

    async def _ack(
        self, consumer: AIOKafkaConsumer, topic_partition: TopicPartition, offset: int
    ) -> None:
        await consumer.commit({topic_partition: offset + 1})

    async def _nack(
        self, consumer: AIOKafkaConsumer, topic_partition: TopicPartition, offset: int
    ) -> None:
        await consumer.seek(topic_partition, offset + 1)
