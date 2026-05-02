import uuid

from fastapi import APIRouter, Depends, HTTPException, Query
from starlette import status

from src.application.dtos.car_dto import CreateCarDTO, UpdateCarDTO
from src.application.services.car_service import CarService
from src.domain.interfaces.task_queue import TaskQueueInterface
from src.interfaces.api.dependencies.services import get_car_service
from src.interfaces.api.dependencies.tasks import get_task_queue
from src.interfaces.api.schemas.car_schemas import (
    CarResponseSchema,
    CarCreateSchema,
    CarUpdateSchema,
)

router = APIRouter(prefix="/cars", tags=["cars"])


@router.post("/", response_model=CarResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_car(
        car_data: CarCreateSchema,
        car_service: CarService = Depends(get_car_service)
):
    create_dto = CreateCarDTO(
        brand=car_data.brand,
        model=car_data.model,
        year=car_data.year,
        price=car_data.price,
    )
    return await car_service.create_car(create_dto)


@router.get("/", response_model=list[CarResponseSchema])
async def get_all_cars(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=1000),
        car_service: CarService = Depends(get_car_service)
):
    return await car_service.get_all_cars(skip=skip, limit=limit)


@router.get("/{car_id}", response_model=CarResponseSchema)
async def get_car(
        car_id: uuid.UUID,
        car_service: CarService = Depends(get_car_service)
):
    car = await car_service.get_car(car_id)
    if car is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Car with id {car_id} not found"
        )
    return car


@router.put("/{car_id}", response_model=CarResponseSchema)
async def update_car(
        car_id: uuid.UUID,
        car_data: CarUpdateSchema,
        car_service: CarService = Depends(get_car_service)
):
    update_dto = UpdateCarDTO(
        brand=car_data.brand,
        model=car_data.model,
        year=car_data.year,
        price=car_data.price,
    )

    updated_car = await car_service.update_car(car_id, update_dto)
    if updated_car is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Car with id {car_id} not found"
        )
    return updated_car


@router.patch("/{car_id}", response_model=CarResponseSchema)
async def partial_update_car(
        car_id: uuid.UUID,
        car_data: CarUpdateSchema,
        car_service: CarService = Depends(get_car_service)
):
    update_dto = UpdateCarDTO(
        brand=car_data.brand,
        model=car_data.model,
        year=car_data.year,
        price=car_data.price,
    )

    updated_car = await car_service.update_car(car_id, update_dto)
    if updated_car is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Car with id {car_id} not found"
        )
    return updated_car


@router.delete("/{car_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_car(
        car_id: uuid.UUID,
        car_service: CarService = Depends(get_car_service)
):
    deleted = await car_service.delete_car(car_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Car with id {car_id} not found"
        )


@router.get("/tasks/{task_id}/status")
async def get_task_status(
    task_id: str,
    task_queue: TaskQueueInterface = Depends(get_task_queue),
):
    result = await task_queue.get_result(task_id)
    if result is None:
        return {"task_id": task_id, "status": "processing"}
    return {"task_id": task_id, "status": "completed", "result": result}
