from typing import Any

from inbound.serializers.base import Serializer


class NoOpSerializer(Serializer):
    @staticmethod
    def serialize(data: Any) -> bytes:
        return data

    @staticmethod
    def deserialize(data: bytes) -> Any:
        return data
