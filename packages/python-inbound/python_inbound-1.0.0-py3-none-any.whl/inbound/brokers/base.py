from abc import ABC, abstractmethod
from typing import Tuple, Type

from inbound.envelope import Envelope
from inbound.event import Event
from inbound.serializers import JSONSerializer, Serializer


class Broker(ABC):
    backend: str

    def __init__(
        self,
        url: str,
        serializer: Type[Serializer] = JSONSerializer,
        node_id: str | None = None,
        *args,
        **kwargs,
    ):
        self.url = url
        self.serializer = serializer

        self._node_id = node_id

    @property
    def node_id(self) -> str | None:
        return self._node_id

    @node_id.setter
    def node_id(self, node_id: str) -> None:
        self._node_id = node_id

    @abstractmethod
    async def connect(self) -> None:
        """
        Connect to the broker
        """
        ...

    @abstractmethod
    async def disconnect(self) -> None:
        """
        Close the connection to the broker
        """
        ...

    @abstractmethod
    async def subscribe(self, channel: str) -> None:
        """
        Subscribe to a specific channel

        :param channel: The name of the channel to subscribe to
        :type channel: str
        """
        ...

    @abstractmethod
    async def unsubscribe(self, channel: str) -> None:
        """
        Unsubscribe from a specific channel

        :param channel: The name of the channel to unsubscribe
        :type channel: str
        """
        ...

    @abstractmethod
    async def publish(self, channel: str, event: Event, **kwargs) -> None:
        """
        Publish an event to a given channel

        :param event: The Event to publish
        :type event: Event
        """
        ...

    @abstractmethod
    async def next(self) -> Tuple[str, Envelope]:
        """
        Get the next event from the broker
        """
        ...
