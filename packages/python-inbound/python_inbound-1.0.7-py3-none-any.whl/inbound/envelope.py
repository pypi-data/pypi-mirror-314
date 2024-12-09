import asyncio
from typing import Awaitable, Callable

from inbound.event import Event


class Envelope:
    def __init__(
        self,
        event: Event,
        ack: Callable[[], Awaitable[None]] | None = None,
        nack: Callable[[], Awaitable[None]] | None = None,
    ) -> None:
        self.event = event
        self._ack = ack
        self._nack = nack
        self._recipient_count = 0
        self._acked_count = 0
        self._nacked = False
        self._lock = asyncio.Lock()

    def add_ack(self, ack: Callable[[], Awaitable[None]]) -> None:
        self._ack = ack

    def add_nack(self, nack: Callable[[], Awaitable[None]]) -> None:
        self._nack = nack

    async def register_recipient(self) -> None:
        async with self._lock:
            self._recipient_count += 1

    async def ack(self) -> None:
        async with self._lock:
            if self._nacked or self._acked_count >= self._recipient_count:
                return

            self._acked_count += 1
            if self._acked_count == self._recipient_count:
                if self._ack:
                    await self._ack()

    async def nack(self) -> None:
        async with self._lock:
            if self._nacked or self._acked_count >= self._recipient_count:
                return

            self._nacked = True
            if self._nack:
                await self._nack()
