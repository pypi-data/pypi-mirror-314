import json
from typing import Any

import orjson

from inbound.serializers.base import Serializer


class JSONSerializer(Serializer):
    @staticmethod
    def serialize(data: Any) -> bytes:
        return json.dumps(data).encode()

    @staticmethod
    def deserialize(data: bytes) -> Any:
        return json.loads(data.decode())


class ORJSONSerializer(Serializer):
    @staticmethod
    def serialize(data: Any) -> bytes:
        return orjson.dumps(data)

    @staticmethod
    def deserialize(data: bytes) -> Any:
        return orjson.loads(data)
