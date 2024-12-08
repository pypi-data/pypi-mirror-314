import asyncio
from functools import partial
from typing import Tuple

from inbound.brokers.base import Broker
from inbound.envelope import Envelope
from inbound.event import Event


class MemoryBroker(Broker):
    """
    An in-memory queue broker
    """

    backend = "memory"

    _channels: set[str] = set()
    _consumer: asyncio.Queue[tuple[str, Envelope]]

    def __init__(self, *args, max_size: int = 100, **kwargs):
        super().__init__(*args, **kwargs)

        self._consumer = asyncio.Queue(max_size)

    async def connect(self) -> None:
        pass

    async def disconnect(self) -> None:
        pass

    async def subscribe(self, channel: str) -> None:
        self._channels.add(channel)

    async def unsubscribe(self, channel: str) -> None:
        if channel in self._channels:
            self._channels.remove(channel)

    async def publish(self, channel: str, event: Event, **kwargs) -> None:
        envelope = Envelope(event)
        envelope.add_ack(partial(self._ack, channel=channel, envelope=envelope))
        envelope.add_nack(partial(self._nack, channel=channel, envelope=envelope))

        await self._consumer.put((channel, envelope))

    async def next(self) -> Tuple[str, Envelope]:
        while True:
            channel, event = await self._consumer.get()
            if channel in self._channels:
                return channel, event

    async def _ack(self, channel: str, envelope: Envelope) -> None:
        self._consumer.task_done()

    async def _nack(self, channel: str, envelope: Envelope) -> None:
        self._consumer.task_done()
        await self._consumer.put((channel, envelope))
