import uuid
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any


class EventType(str, Enum):
    CAR_CREATED = "CAR_CREATED"
    CAR_UPDATED = "CAR_UPDATED"
    CAR_DELETED = "CAR_DELETED"


@dataclass
class CarEventDTO:
    event_id: uuid.UUID
    event_type: EventType
    car_id: uuid.UUID
    timestamp: datetime
    data: dict[str, Any]

    def to_dict(self) -> dict:
        return {
            "event_id": str(self.event_id),
            "event_type": self.event_type.value,
            "car_id": str(self.car_id),
            "timestamp": self.timestamp.isoformat(),
            "data": self.data
        }

    @classmethod
    def from_dict(cls, data: dict) -> "CarEventDTO":
        return cls(
            event_id=uuid.UUID(data["event_id"]),
            event_type=EventType(data["event_type"]),
            car_id=uuid.UUID(data["car_id"]),
            timestamp=datetime.fromisoformat(data["timestamp"]),
            data=data["data"],
        )
