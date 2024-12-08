from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class Serializer(Protocol):
    @staticmethod
    def serialize(data: Any) -> bytes: ...

    @staticmethod
    def deserialize(data: bytes) -> Any: ...
