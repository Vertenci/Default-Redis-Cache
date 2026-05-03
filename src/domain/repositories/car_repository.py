import uuid
from abc import ABC, abstractmethod

from src.domain.entities.car import Car


class CarRepository(ABC):
    @abstractmethod
    async def save(self, car: Car) -> Car:
        pass

    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> list[Car]:
        pass

    @abstractmethod
    async def get_by_id(self, car_id: uuid.UUID) -> Car | None:
        pass

    @abstractmethod
    async def delete(self, car_id: uuid.UUID) -> bool:
        pass
