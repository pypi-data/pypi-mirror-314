from collections import namedtuple
from datetime import datetime, timezone
from typing import Any, Type, TypeVar

from cloudevents.pydantic import CloudEvent
from cloudevents.pydantic import from_dict as cloud_event_from_dict


EventType = TypeVar("EventType", bound="Event")
BaseEvent = namedtuple("BaseEvent", ["type", "data", "headers"], defaults=[..., ..., {}])


class Event(BaseEvent):
    @classmethod
    def from_cloud_event(cls: Type[EventType], event: CloudEvent | dict) -> EventType:
        if isinstance(event, dict):
            event = cloud_event_from_dict(event)

        headers = {k: str(v) for k, v in event.get_attributes().items() if v is not None}

        return cls(
            type=headers.pop("type"),
            headers=headers,
            data=event.get_data(),
        )

    def to_cloud_event(self) -> CloudEvent:
        return CloudEvent.create({"type": self.type, **self.headers}, self.data)

    @classmethod
    def create(
        cls: Type[EventType],
        type: str,
        data: Any,
        headers: dict[str, str] | None = None,
    ) -> EventType:
        headers = headers or {}

        if not headers.get("time", None):
            headers["time"] = datetime.now(timezone.utc).isoformat()

        return cls(type=type, data=data, headers=headers)
