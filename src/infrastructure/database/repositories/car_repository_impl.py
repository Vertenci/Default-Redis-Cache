import uuid
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.entities.car import Car
from src.domain.repositories.car_repository import CarRepository
from src.infrastructure.database.models.car_model import CarModel


class CarRepositoryImpl(CarRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def save(self, car: Car) -> Car:
        if car.id is None:
            car_model = CarModel(
                brand=car.brand,
                model=car.model,
                year=car.year,
                price=car.price,
                created_at=car.created_at,
                updated_at=car.updated_at,
            )
            self._session.add(car_model)
            await self._session.flush()
            await self._session.refresh(car_model)
            await self._session.commit()
        else:
            stmt = select(CarModel).where(CarModel.id == car.id)
            result = await self._session.execute(stmt)
            car_model = result.scalar_one()

            car_model.brand = car.brand
            car_model.model = car.model
            car_model.year = car.year
            car_model.price = car.price
            car_model.updated_at = car.updated_at

            await self._session.flush()
            await self._session.refresh(car_model)
            await self._session.commit()

        return self._to_entity(car_model)

    async def get_by_id(self, car_id: uuid.UUID) -> Car | None:
        stmt = select(CarModel).where(CarModel.id == car_id)
        result = await self._session.execute(stmt)
        car_model = result.scalar_one_or_none()
        return self._to_entity(car_model) if car_model else None

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[Car]:
        stmt = select(CarModel).offset(skip).limit(limit)
        result = await self._session.execute(stmt)
        car_models = result.scalars().all()
        return [self._to_entity(model) for model in car_models]

    async def delete(self, car_id: uuid.UUID) -> bool:
        stmt = delete(CarModel).where(CarModel.id == car_id)
        result = await self._session.execute(stmt)
        await self._session.flush()
        await self._session.commit()
        return result.rowcount > 0

    @staticmethod
    def _to_entity(model: CarModel) -> Car:
        return Car(
            id=model.id,
            brand=model.brand,
            model=model.model,
            year=model.year,
            price=model.price,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
