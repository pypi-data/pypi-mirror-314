from __future__ import annotations

import asyncio
from typing import Awaitable, Callable, TypeVar

from inbound.envelope import Envelope
from inbound.event import Event
from inbound.utils import is_async_callable, is_sync_callable


R = TypeVar("R")

CallbackType = Callable[[Event], R | Awaitable[R]]
ErrorCallbackType = Callable[[BaseException, Event], R | Awaitable[R]]


class EventCallback:
    def __init__(
        self,
        channel: str,
        event_type: str,
        fn: CallbackType,
        err_fn: ErrorCallbackType | None = None,
    ):
        if not callable(fn):
            raise TypeError("`fn` must be callable.")
        if err_fn and not callable(err_fn):
            raise TypeError("`err_fn` must be callable.")

        assert channel, "EventCallback `channel` must not be empty"
        assert event_type, "EventCallback `event_type` must not be empty"

        self._fn = fn
        self._err_fn = err_fn
        self._name = self._fn.__name__
        self._channel = channel
        self._event_type = event_type

    @property
    def channel(self) -> str:
        return self._channel

    @property
    def event_type(self) -> str:
        return self._event_type

    @property
    def name(self) -> str:
        return self._name

    def match_event_type(self, event_type: str) -> bool:
        return self.event_type == event_type or self.event_type == "*"

    async def __call__(self, envelope: Envelope) -> R | None:
        try:
            if is_async_callable(self._fn):
                return await self._fn(envelope.event)
            elif is_sync_callable(self._fn):
                return await asyncio.to_thread(self._fn, envelope.event)
            return None
        except Exception as e:
            if self._err_fn:
                if is_async_callable(self._err_fn):
                    return await self._err_fn(e, envelope.event)
                elif is_sync_callable(self._err_fn):
                    return await asyncio.to_thread(self._err_fn, e, envelope.event)
            raise e


class CallbackGroup:
    def __init__(
        self,
        error_handler: ErrorCallbackType | None = None,
        callback_cls: type[EventCallback] = EventCallback,
    ) -> None:
        self._error_handler = error_handler
        self._callback_cls = callback_cls
        self._callbacks: dict[str, list[EventCallback]] = {}

    @property
    def callbacks(self):
        return self._callbacks

    @property
    def channels(self):
        return self._callbacks.keys()

    def add_group(self, group: CallbackGroup) -> None:
        """
        Add a group of callbacks to the current group.

        :param group: The group of callbacks to add
        :type group: CallbackGroup
        """
        for _, callbacks in group.callbacks.items():
            for callback in callbacks:
                self.register_callback(callback)

    def get_callbacks(self, channel: str, event_type: str) -> list[EventCallback]:
        """
        Get all callbacks that match the channel and event_type.

        :param channel: The channel to match
        :type channel: str
        :param event_type: The event_type to match
        :type event_type: str
        :return: A list of callbacks that match the channel and event_type
        :rtype: list[EventCallback]
        """
        return [
            callback
            for callback in self.callbacks.get(channel, [])
            if callback.match_event_type(event_type)
        ]

    def remove_callback(self, callback: EventCallback) -> None:
        """
        Remove a callback from the group.

        :param callback: The callback to remove
        :type callback: EventCallback
        """
        self._callbacks[callback.channel].remove(callback)
        if not self._callbacks[callback.channel]:
            del self._callbacks[callback.channel]

    def register_callback(self, callback: EventCallback) -> None:
        """
        Register a callback to the group.

        :param callback: The callback to register
        :type callback: EventCallback
        """
        if callback.channel in self._callbacks.keys():
            self._callbacks[callback.channel].append(callback)
        else:
            self._callbacks[callback.channel] = [callback]

    def add_callback(
        self,
        channel: str,
        event_type: str,
        callback: CallbackType,
        err_callback: ErrorCallbackType | None = None,
    ) -> EventCallback:
        """
        Add a callback to the group.

        :param channel: The channel to match
        :type channel: str
        :param event_type: The event_type to match
        :type event_type: str
        :param callback: The callback to add
        :type callback: CallbackType
        :param err_callback: The error callback to add
        :type err_callback: ErrorCallbackType
        """
        event_callback = self._callback_cls(
            channel=channel,
            event_type=event_type,
            fn=callback,
            err_fn=err_callback or self._error_handler,
        )
        self.register_callback(event_callback)
        return event_callback

    def callback(self, channel: str, event_type: str) -> Callable[[CallbackType], EventCallback]:
        """
        Decorator to add a callback to the group.

        :param channel: The channel to match
        :type channel: str
        :param event_type: The event_type to match
        :type event_type: str
        :return: The decorator
        :rtype: Callable[[CallbackType], CallbackType]
        """

        def decorator(func: CallbackType) -> EventCallback:
            return self.add_callback(channel=channel, event_type=event_type, callback=func)

        return decorator
