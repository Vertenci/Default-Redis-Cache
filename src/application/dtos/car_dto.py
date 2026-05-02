import uuid
from dataclasses import dataclass
from datetime import datetime


@dataclass
class CreateCarDTO:
    brand: str
    model: str
    year: int
    price: int


@dataclass
class UpdateCarDTO:
    brand: str | None
    model: str | None
    year: int | None
    price: int | None


@dataclass
class CarResponseDTO:
    id: uuid.UUID
    brand: str
    model: str
    year: int
    price: int
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, car) -> "CarResponseDTO":
        return cls(
            id=car.id if car.id is not None else 0,
            brand=car.brand,
            model=car.model,
            year=car.year,
            price=car.price,
            created_at=car.created_at,
            updated_at=car.updated_at,
        )
