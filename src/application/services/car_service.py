import uuid

from datetime import datetime

from src.application.dtos.car_dto import CreateCarDTO, CarResponseDTO, UpdateCarDTO
from src.domain.entities.car import Car
from src.domain.interfaces.cache import CacheInterface
from src.domain.interfaces.task_queue import TaskQueueInterface
from src.domain.repositories.car_repository import CarRepository


class CarService:
    CACHE_KEY_PREFIX = "car"
    CACHE_KEY_LIST = "cars"
    CACHE_TTL = 300

    def __init__(self, car_repository: CarRepository, cache: CacheInterface | None = None, task_queue: TaskQueueInterface | None = None):
        self._car_repository = car_repository
        self._cache = cache
        self._task_queue  = task_queue

    def _cache_key(self, car_id: uuid.UUID) -> str:
        return f"{self.CACHE_KEY_PREFIX}:{car_id}"

    def _list_cache_key(self, skip: int, limit: int) -> str:
        return f"{self.CACHE_KEY_LIST}:{skip}:{limit}"

    @staticmethod
    def _dto_to_dict(dto: CarResponseDTO) -> dict:
        return {
            "id": str(dto.id),
            "brand": dto.brand,
            "model": dto.model,
            "year": dto.year,
            "price": dto.price,
            "created_at": dto.created_at.isoformat(),
            "updated_at": dto.updated_at.isoformat(),
        }

    @staticmethod
    def _dict_to_dto(data: dict) -> CarResponseDTO:
        return CarResponseDTO(
            id=uuid.UUID(data["id"]),
            brand=data["brand"],
            model=data["model"],
            year=data["year"],
            price=data["price"],
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
        )

    async def create_car(self, create_dto: CreateCarDTO) -> CarResponseDTO:
        car = Car.create(
            brand=create_dto.brand,
            model=create_dto.model,
            year=create_dto.year,
            price=create_dto.price
        )
        saved_car = await self._car_repository.save(car)
        response = CarResponseDTO.from_entity(saved_car)

        if self._task_queue:
            task_id = await self._task_queue.send_task(
                "car_tasks.send_car_created_notification",
                car_id=str(saved_car.id),
                brand=saved_car.brand,
                model=saved_car.model,
                email="admin@example.com",
            )

        if self._cache:
            await self._cache.delete_pattern(f"{self.CACHE_KEY_LIST}:*")

        return response

    async def get_car(self, car_id: uuid.UUID) -> CarResponseDTO | None:
        if self._cache:
            cache_key = self._cache_key(car_id)
            cached = await self._cache.get(cache_key)
            if cached is not None:
                return self._dict_to_dto(cached)

        car = await self._car_repository.get_by_id(car_id)
        if car is None:
            return None

        response = CarResponseDTO.from_entity(car)

        if self._cache:
            await self._cache.set(
                self._cache_key(car_id),
                self._dto_to_dict(response),
                ttl=self.CACHE_TTL,
            )

        return response

    async def get_all_cars(self, skip: int = 0, limit: int = 100) -> list[CarResponseDTO]:
        cache_key = self._list_cache_key(skip, limit)

        if self._cache:
            cached = await self._cache.get(cache_key)
            if cached is not None:
                return [self._dict_to_dto(item) for item in cached]

        cars = await self._car_repository.get_all(skip, limit)
        response_list = [CarResponseDTO.from_entity(car) for car in cars]

        if self._cache:
            await self._cache.set(
                cache_key,
                [self._dto_to_dict(item) for item in response_list],
                ttl=self.CACHE_TTL,
            )

        return response_list

    async def update_car(self, car_id: uuid.UUID, update_dto: UpdateCarDTO) -> CarResponseDTO | None:
        car = await self._car_repository.get_by_id(car_id)
        if car is None:
            return None

        car.update(
            brand=update_dto.brand,
            model=update_dto.model,
            year=update_dto.year,
            price=update_dto.price,
        )

        updated_car = await self._car_repository.save(car)
        response = CarResponseDTO.from_entity(updated_car)

        if self._cache:
            await self._cache.set(
                self._cache_key(car_id),
                self._dto_to_dict(response),
                ttl=self.CACHE_TTL,
            )
            await self._cache.delete_pattern(f"{self.CACHE_KEY_LIST}:*")

        return response

    async def delete_car(self, car_id: uuid.UUID) -> bool:
        deleted = await self._car_repository.delete(car_id)
        if deleted and self._cache:
            await self._cache.delete(self._cache_key(car_id))
            await self._cache.delete_pattern(f"{self.CACHE_KEY_LIST}:*")

        return deleted
