import uuid
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Car:
    id: uuid.UUID | None
    brand: str
    model: str
    year: int
    price: int
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    @classmethod
    def create(cls, brand: str, model: str, year: int, price: int) -> "Car":
        if not brand.strip():
            raise ValueError("Brand cannot be empty")
        if not model.strip():
            raise ValueError("Model cannot be empty")
        if year < 1886:
            raise ValueError("Invalid year")
        if price <= 0:
            raise ValueError("Price must be positive")

        return cls(
            id=None,
            brand=brand,
            model=model,
            year=year,
            price=price,
        )

    def update(self, brand: str | None = None, model: str | None = None,
               year: int | None = None, price: int | None = None) -> None:
        if brand is not None:
            if not brand.strip():
                raise ValueError("Brand cannot be empty")
            self.brand = brand.strip()
        if model is not None:
            if not model.strip():
                raise ValueError("Model cannot be empty")
            self.model = model.strip()
        if year is not None:
            if year < 1886:
                raise ValueError("Invalid year")
            self.year = year
        if price is not None:
            if price <= 0:
                raise ValueError("Price must be positive")
            self.price = price
        self.updated_at = datetime.now()
