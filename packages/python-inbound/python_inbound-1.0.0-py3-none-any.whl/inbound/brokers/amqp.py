import asyncio
from typing import Tuple, Type

import aio_pika

from inbound.brokers.base import Broker
from inbound.envelope import Envelope
from inbound.event import Event
from inbound.serializers import JSONSerializer, Serializer
from inbound.utils import cancel_task


class AMQPBroker(Broker):
    """
    An AMQP Broker using `aio_pika` as the underlying library.
    """

    backend = "amqp"

    _channel_consumers: dict[str, asyncio.Task] = {}
    _inbound_queue: asyncio.Queue[tuple[str, Envelope]]
    _connection: aio_pika.abc.AbstractRobustConnection
    _producer: aio_pika.abc.AbstractChannel

    def __init__(
        self,
        url: str,
        serializer: Type[Serializer] = JSONSerializer,
        node_id: str | None = None,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(url, serializer, node_id, *args, **kwargs)
        self._args = args
        self._kwargs = kwargs

    async def _consume_channel(self, queue: aio_pika.abc.AbstractQueue):
        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                event = Event(
                    type=message.headers.pop("x-event-type"),
                    headers=message.headers,
                    data=self.serializer.deserialize(message.body),
                )
                await self._inbound_queue.put(
                    (
                        queue.name,
                        Envelope(
                            event,
                            ack=message.ack,
                            nack=message.nack,
                        ),
                    )
                )

    async def connect(self) -> None:
        self._inbound_queue = asyncio.Queue()
        self._connection = await aio_pika.connect_robust(self.url, *self._args, **self._kwargs)
        self._producer = await self._connection.channel()

    async def disconnect(self) -> None:
        for channel in list(self._channel_consumers.keys()):
            await self.unsubscribe(channel)
        await self._connection.close()

    async def subscribe(self, channel: str) -> None:
        if not self._channel_consumers.get(channel):
            _channel = await self._connection.channel()
            _queue = await _channel.declare_queue(channel, auto_delete=True)

            self._channel_consumers[channel] = asyncio.create_task(self._consume_channel(_queue))

    async def unsubscribe(self, channel: str) -> None:
        if task := self._channel_consumers.get(channel):
            del self._channel_consumers[channel]
            await cancel_task(task)

    async def publish(self, channel: str, event: Event, **kwargs) -> None:
        headers = event.headers or {}
        headers["x-event-type"] = event.type

        await self._producer.default_exchange.publish(
            aio_pika.Message(body=self.serializer.serialize(event.data), headers=headers, **kwargs),
            routing_key=channel,
            **kwargs,
        )

    async def next(self) -> Tuple[str, Envelope]:
        return await self._inbound_queue.get()
