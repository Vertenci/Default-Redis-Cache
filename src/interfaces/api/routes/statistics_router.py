from fastapi import APIRouter, Depends, Query

from src.application.services.statistics_service import StatisticsService
from src.interfaces.api.dependencies.services import get_statistics_service

router = APIRouter(prefix="/cars/s", tags=["statistics"])


@router.get("/statistics")
async def get_statistics(
    service: StatisticsService = Depends(get_statistics_service),
):
    return await service.get_statistics()


@router.get("/statistics/events")
async def get_events(
    limit: int = Query(20, ge=1, le=100),
    service: StatisticsService = Depends(get_statistics_service),
):
    return await service.get_recent_events(limit)
