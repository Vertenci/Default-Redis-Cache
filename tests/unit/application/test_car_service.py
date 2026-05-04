import uuid
import pytest
from unittest.mock import AsyncMock

from src.application.dtos.car_dto import CreateCarDTO
from src.application.services.car_service import CarService
from src.domain.entities.car import Car


class TestCarService:
    @pytest.fixture
    def mock_repository(self):
        return AsyncMock()

    @pytest.fixture
    def car_service(self, mock_repository, fake_cache, fake_task_queue):
        return CarService(mock_repository, fake_cache, fake_task_queue)

    async def test_create_car(self, car_service, mock_repository):
        car_id = uuid.uuid4()
        car = Car(id=car_id, brand="BMW", model="X5", year=2024, price=50000)
        mock_repository.save.return_value = car
        dto = CreateCarDTO(brand="BMW", model="X5", year=2024, price=50000)

        result = await car_service.create_car(dto)

        assert result.brand == "BMW"
        assert result.id == car_id
        mock_repository.save.assert_called_once()

    async def test_get_car_from_cache(self, car_service, fake_cache):
        car_id = uuid.uuid4()
        fake_cache._store[f"car:{car_id}"] = {
            "id": str(car_id),
            "brand": "BMW",
            "model": "X5",
            "year": 2024,
            "price": 50000,
            "created_at": "2024-01-01T00:00:00",
            "updated_at": "2024-01-01T00:00:00",
        }

        result = await car_service.get_car(car_id)
        assert result.brand == "BMW"

    async def test_delete_car_invalidates_cache(self, car_service, mock_repository, fake_cache):
        car_id = uuid.uuid4()
        mock_repository.delete.return_value = True
        fake_cache._store[f"car:{car_id}"] = {}
        fake_cache._store["cars:0:100"] = []

        result = await car_service.delete_car(car_id)

        assert result is True
        assert f"car:{car_id}" not in fake_cache._store
        assert "cars:0:100" not in fake_cache._store
