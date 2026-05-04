from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.services.car_service import CarService
from src.application.services.statistics_service import StatisticsService
from src.domain.interfaces.cache import CacheInterface
from src.domain.interfaces.event_publisher import EventPublisherInterface
from src.domain.interfaces.task_queue import TaskQueueInterface
from src.infrastructure.database.repositories.car_repository_impl import CarRepositoryImpl
from src.interfaces.api.dependencies.cache import get_cache
from src.interfaces.api.dependencies.database import get_db_session
from src.interfaces.api.dependencies.event_publisher import get_event_publisher
from src.interfaces.api.dependencies.tasks import get_task_queue


async def get_car_service(
        session: AsyncSession = Depends(get_db_session),
        cache: CacheInterface = Depends(get_cache),
        task_queue: TaskQueueInterface = Depends(get_task_queue),
        event_publisher: EventPublisherInterface = Depends(get_event_publisher),
) -> CarService:
    car_repository = CarRepositoryImpl(session)
    return CarService(car_repository, cache, task_queue, event_publisher)

async def get_statistics_service(
        cache: CacheInterface = Depends(get_cache),
)-> StatisticsService:
    return StatisticsService(cache)
