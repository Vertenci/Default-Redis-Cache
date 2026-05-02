from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.services.car_service import CarService
from src.domain.interfaces.cache import CacheInterface
from src.infrastructure.database.repositories.car_repository_impl import CarRepositoryImpl
from src.interfaces.api.dependencies.cache import get_cache
from src.interfaces.api.dependencies.database import get_db_session


async def get_car_service(session: AsyncSession = Depends(get_db_session), cache: CacheInterface = Depends(get_cache)) -> CarService:
    car_repository = CarRepositoryImpl(session)
    return CarService(car_repository, cache)
