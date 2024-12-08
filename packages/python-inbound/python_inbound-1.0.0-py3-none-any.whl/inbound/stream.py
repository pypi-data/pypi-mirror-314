import asyncio
from typing import AsyncIterator, Literal

from inbound.envelope import Envelope


class SentinelMeta(type):
    def __init__(cls, name, bases, dict):
        super(SentinelMeta, cls).__init__(name, bases, dict)
        cls._instance = None

    def __call__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SentinelMeta, cls).__call__(*args, **kwargs)
        return cls._instance

    def __repr__(cls) -> str:
        return f"<{cls.__name__}>"

    def __bool__(cls) -> Literal[False]:
        return False


class EndOfStream(metaclass=SentinelMeta):
    pass


class StreamFinished(Exception): ...


class EventStream:
    def __init__(
        self,
        *,
        maxsize: int = 0,
    ) -> None:
        """
        Helper class to allow consuming events from an inbound queue as an iterator.

        :param maxsize: The maxsize of the internal queue
        :type maxsize: int
        """
        self._queue: asyncio.Queue[Envelope | EndOfStream] = asyncio.Queue(maxsize)
        self._closed: asyncio.Event = asyncio.Event()

    @property
    def closed(self) -> bool:
        """
        Return True if the stream is closed.
        """
        return self._closed.is_set()

    async def __aiter__(self) -> AsyncIterator[Envelope]:
        # Iterate over the event in the queue and yield them
        # Finish iteration when StreamFinished is reached
        try:
            while event := await self.get():
                yield event
        except (StreamFinished, asyncio.CancelledError):
            self._closed.set()

    async def get(self) -> Envelope:
        """
        Get an Event dict from the stream.
        Raises StreamFinished when EndOfStream is encountered.
        """
        if (event := await self._queue.get()) and not isinstance(event, EndOfStream):
            self._queue.task_done()
            return event

        raise StreamFinished

    async def put(self, item: Envelope | EndOfStream) -> None:
        """
        Put an Event envelope or EndOfStream on the stream.

        :param item: The Event envelope or EndOfStream
        :type item: Envelope | EndOfStream
        """
        if (not isinstance(item, Envelope)) and (not isinstance(item, EndOfStream)):
            raise ValueError("`item` must be an Event or EndOfStream")

        await self._queue.put(item)

    async def close(self) -> None:
        """
        Signal a close to the stream with an EndOfStream.
        """
        await self.put(EndOfStream())
