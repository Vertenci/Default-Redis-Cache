import uuid
from src.domain.entities.car import Car
from src.infrastructure.database.repositories.car_repository_impl import CarRepositoryImpl


class TestCarRepository:
    async def test_save_new_car(self, test_session):
        repo = CarRepositoryImpl(test_session)
        car = Car.create(brand="BMW", model="X5", year=2024, price=50000)
        saved = await repo.save(car)
        assert saved.id is not None
        assert saved.brand == "BMW"

    async def test_get_by_id_not_found(self, test_session):
        repo = CarRepositoryImpl(test_session)
        result = await repo.get_by_id(uuid.uuid4())
        assert result is None

    async def test_get_all_with_pagination(self, test_session):
        repo = CarRepositoryImpl(test_session)
        for i in range(3):
            car = Car.create(brand=f"Brand{i}", model=f"Model{i}", year=2024, price=10000)
            await repo.save(car)

        result = await repo.get_all(skip=0, limit=2)
        assert len(result) == 2

        result = await repo.get_all(skip=2, limit=2)
        assert len(result) == 1

    async def test_delete_existing(self, test_session):
        repo = CarRepositoryImpl(test_session)
        car = Car.create(brand="BMW", model="X5", year=2024, price=50000)
        saved = await repo.save(car)

        deleted = await repo.delete(saved.id)
        assert deleted is True

        result = await repo.get_by_id(saved.id)
        assert result is None
