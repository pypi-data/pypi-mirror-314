import asyncio
import logging
from contextlib import asynccontextmanager
from typing import Any, AsyncIterator, Literal, TypeVar
from uuid import uuid4

from inbound.brokers import Broker, MemoryBroker
from inbound.callback import CallbackGroup, EventCallback
from inbound.envelope import Envelope
from inbound.event import Event
from inbound.serializers.noop import NoOpSerializer
from inbound.stream import EventStream
from inbound.utils import cancel_task, gather_with_concurrency


logger = logging.getLogger(__name__)

TEventBus = TypeVar("TEventBus", bound="EventBus")


class EventBus:
    def __init__(
        self,
        broker: Broker | None = None,
        node_id: str | None = None,
        concurrency_limit: int = 100,
    ):
        assert asyncio.get_running_loop(), "EventBus must be instantiated with an active loop"

        self._node_id = node_id or f"inbound-{uuid4()}"
        self._broker = broker or MemoryBroker(
            "memory://", serializer=NoOpSerializer(), max_size=1000
        )
        self._concurrency_limit = concurrency_limit

        self._lock = asyncio.Lock()
        self._disconnected = asyncio.Event()
        self._disconnected.set()

        self._consumer_task: asyncio.Task | None = None

        self._streams: dict[str, set[EventStream]] = {}
        self._callback_tasks: dict[str, set[asyncio.Task]] = {}
        self._callback_group: CallbackGroup = CallbackGroup()

        if not self._broker.node_id and self.node_id:
            self._broker.node_id = self.node_id

    @property
    def connected(self) -> bool:
        return not self._disconnected.is_set()

    @property
    def broker(self) -> Broker:
        return self._broker

    @property
    def node_id(self) -> str:
        return self._node_id

    def _ensure_connected(self):
        if not self.connected:
            raise RuntimeError("Must call `.connect` on the EventBus")

    async def _consumer(self):
        # Iteratively get the incoming events and add them
        # to their respective streams
        while True:
            channel, envelope = await self._broker.next()
            streams = self._streams.get(channel, set()) | self._streams.get("*", set())

            for stream in streams:
                await envelope.register_recipient()
                await stream.put(envelope)

    async def _create_callback_reader(self, channel):
        # Create callback reader task
        self._callback_tasks[channel] = asyncio.create_task(self._read_stream(channel))

    async def create_callback_reader(self, channel):
        async with self.lock:
            await self._create_callback_reader(channel)

    async def _read_stream(self, channel: str) -> None:
        # Subscribe to the channel and call the callbacks
        # for each event
        # Task will end when the stream is closed
        async with self.subscribe(channel) as stream:
            async for envelope in stream:
                try:
                    await self._fire_callbacks(
                        self._callback_group.get_callbacks(channel, envelope.event.type), envelope
                    )
                    await envelope.ack()
                except BaseException:
                    await envelope.nack()

    async def _fire_callbacks(self, callbacks: list[EventCallback], envelope: Envelope) -> None:
        await gather_with_concurrency(
            self._concurrency_limit,
            *(callback(envelope) for callback in callbacks),
        )

    def add_group(self, group: CallbackGroup) -> None:
        """
        Add a CallbackGroup to the EventBus group

        :param group: The callback group to add
        :type group: CallbackGroup
        """
        assert isinstance(group, CallbackGroup)
        self._callback_group.add_group(group)

    async def connect(self) -> None:
        """
        Initiate the connection for the EventBus
        """
        async with self._lock:
            # As long as we aren't already connected
            if not self.connected:
                # Connect on the broker
                await self._broker.connect()

                # Create callback readers for each channel in group
                for channel in self._callback_group.channels:
                    await self._create_callback_reader(channel)

                # Create our reader task
                self._consumer_task = asyncio.create_task(self._consumer())

                # Set connected flag
                self._disconnected.clear()
                await asyncio.sleep(1)

    async def disconnect(self) -> None:
        """
        Disconnect the EventBus
        """
        async with self._lock:
            await self.close_streams()

            # Cancel task if not done
            if self._consumer_task and not self._consumer_task.done():
                await cancel_task(self._consumer_task)

            await self._broker.disconnect()
            self._disconnected.set()

    async def __aenter__(self: TEventBus) -> TEventBus:
        await self.connect()
        return self

    async def __aexit__(self, *exc) -> None:
        await self.disconnect()

    async def wait_until_finished(self) -> Literal[True]:
        """
        Wait until the EventBus is finished
        """
        return await self._disconnected.wait()

    async def _subscribe_channel(self, channel: str) -> None:
        await self._broker.subscribe(channel)

    async def _unsubscribe_channel(self, channel: str) -> None:
        await self._broker.unsubscribe(channel)

    async def _register_stream(self, channel: str, stream: EventStream) -> None:
        # Check if there is already a subscriber for this channel
        if not self._streams.get(channel):
            # If no existing subscriber, add one and subscribe on the broker
            await self._subscribe_channel(channel)
            self._streams[channel] = {
                stream,
            }
        else:
            # If there is, simply add it
            self._streams[channel].add(stream)

    async def register_stream(self, channel: str, stream: EventStream) -> None:
        """
        Register a stream to receive events from a channel

        :param channel: The channel to subscribe to
        :type channel: str
        :param stream: The stream to register
        :type stream: EventStream
        """
        async with self._lock:
            await self._register_stream(channel, stream)

    async def _deregister_stream(self, channel: str, stream: EventStream) -> None:
        # Get all of the subscriber stream for this channel
        if stream_set := self._streams.get(channel):
            # Remove it from the set
            stream_set.remove(stream)
            # If the set is now empty, we have no more subscribers for this channel
            if not stream_set:
                # Delete the set
                del self._streams[channel]
                # And unsubscribe from the broker
                await self._unsubscribe_channel(channel)

    async def deregister_stream(self, channel: str, stream: EventStream) -> None:
        """
        Deregister a stream from receiving events from a channel

        :param channel: The channel to unsubscribe from
        :type channel: str
        :param stream: The stream to deregister
        :type stream: EventStream
        """
        async with self._lock:
            await self._deregister_stream(channel, stream)

    async def close_streams(self) -> None:
        """
        Close all streams
        """
        # Put a Sentinel on all streams to close them
        for streams in self._streams.values():
            for stream in streams:
                await stream.close()

    async def publish(
        self, channel: str, type: str, data: dict, headers: dict | None = None, **kwargs
    ) -> None:
        """
        Publish an Event to the Broker

        :param channel: The channel to publish to
        :type channel: str
        :param type: The type of the event
        :type type: str
        :param data: The data to publish
        :type data: dict
        :param headers: The headers for the event
        :type headers: dict
        """
        # Publish the Event on the broker
        await self.publish_event(
            channel=channel,
            event=Event.create(type=type, data=data, headers=headers or {}),
            **kwargs,
        )

    async def publish_event(self, channel: str, event: Event, **kwargs) -> None:
        """
        Publish an Event to the Broker

        :param channel: The channel to publish to
        :type channel: str
        :param event: The Event to publish
        :type event: Event
        """
        self._ensure_connected()

        if not event.headers.get("source", None):
            event.headers["source"] = self._node_id

        # Publish the Event on the broker
        await self._broker.publish(channel, event, **kwargs)

    async def request(
        self,
        channel: str,
        type: str,
        data: dict,
        headers: dict | None = None,
        *,
        return_envelope: bool = False,
        **kwargs,
    ) -> Any:
        """
        Send a Request style Event and wait for the
        response.

        :param channel: The channel to publish to
        :type channel: str
        :param type: The type of the event
        :type type: str
        :param data: The data to publish
        :type data: dict
        :param headers: The headers for the event
        :type headers: dict | None
        :param return_envelope: Return the Envelope instead of the data
        :type return_envelope: bool
        :returns: The ReplyEvent or None
        """
        headers = headers or {}

        if not headers.get("correlation_id", None):
            headers["correlation_id"] = str(uuid4())

        if not headers.get("reply_channel", None):
            headers["reply_channel"] = headers["correlation_id"] + "-response"

        response_task = asyncio.create_task(
            self.watch_for_event(
                channel=headers["reply_channel"],
                conditions={"correlation_id": headers["correlation_id"]},
            )
        )

        await self.publish(channel=channel, type=type, data=data, headers=headers, **kwargs)

        if response := await response_task:
            if return_envelope:
                return response
            return response.event.data

        return None

    async def reply(self, event: Event, data: dict, headers: dict | None = None, **kwargs) -> None:
        """
        Reply to a Request style Event

        :param event: The Event to reply to
        :type event: Event
        :param data: The data to publish
        :type data: dict
        :param headers: The headers for the event
        :type headers: dict | None
        """
        headers = headers or {}

        if not headers.get("correlation_id", None):
            headers["correlation_id"] = event.headers["correlation_id"]

        if not headers.get("reply_channel", None):
            headers["reply_channel"] = event.headers["reply_channel"]

        await self.publish(
            channel=event.headers["reply_channel"],
            type=event.type,
            data=data,
            headers=headers,
            **kwargs,
        )

    @asynccontextmanager
    async def subscribe(self, channel: str, **kwargs) -> AsyncIterator[EventStream]:
        """
        Context manager to create an EventStream and subscribe to the specified channel.

        :param channel: The channel to subscribe to
        :type channel: str
        :param **kwargs: The keyword args to pass to the EventStream
        :type **kwargs: Any
        """
        self._ensure_connected()

        stream = EventStream(**kwargs)
        # Register the stream
        await self._register_stream(channel, stream)
        try:
            yield stream
        finally:
            # Put sentinel to signal end
            await stream.close()
            # Deregister the stream
            await self._deregister_stream(channel, stream)

    async def watch_for_event(
        self,
        channel: str,
        event_type: str = "*",
        conditions: dict[str, Any] | None = None,
    ) -> Envelope | None:
        """
        Subscribe to a channel and watch for an event based on certain
        conditions.

        :param channel: The channel to subscribe to
        :type channel: str
        :param event_type: The type of event to watch for, defaults to any
        :type event_type: str
        :param conditions: A dictionary of expected headers in the Event
        :type conditions: dict[str, Any]
        :returns: The matching Envelope or None
        """
        conditions = conditions or {}

        async with self.subscribe(channel) as stream:
            async for envelope in stream:
                # For each event we see, if it's the correct type
                # and has all of the matching headers, then return it
                has_headers = all(
                    True if envelope.event.headers.get(key) == value else False
                    for key, value in conditions.items()
                )
                correct_type = event_type == "*" or envelope.event.type == event_type

                if has_headers and correct_type:
                    return envelope

        return None
