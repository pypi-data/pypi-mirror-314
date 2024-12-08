from typing import Any

import msgpack

from inbound.serializers.base import Serializer


class MsgPackSerializer(Serializer):
    @staticmethod
    def serialize(data: Any) -> bytes:
        return msgpack.packb(data)

    @staticmethod
    def deserialize(data: bytes) -> Any:
        return msgpack.unpackb(data)
