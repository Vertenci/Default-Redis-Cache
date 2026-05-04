import uuid
from unittest.mock import AsyncMock, patch

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.infrastructure.database.base import Base
from src.infrastructure.database.database import db_manager
from src.main import app


@pytest.fixture
async def test_engine():
    engine = create_async_engine("sqlite+aiosqlite:///", echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest.fixture
async def async_client(test_engine):
    original_factory = db_manager._async_session_maker
    original_engine = db_manager._engine

    db_manager._engine = test_engine
    db_manager._async_session_maker = async_sessionmaker(
        test_engine, class_=AsyncSession, expire_on_commit=False
    )

    with (
        patch("src.interfaces.api.dependencies.cache.RedisCache.get", new_callable=AsyncMock, return_value=None),
        patch("src.interfaces.api.dependencies.cache.RedisCache.set", new_callable=AsyncMock, return_value=True),
        patch("src.interfaces.api.dependencies.cache.RedisCache.delete", new_callable=AsyncMock, return_value=1),
        patch("src.interfaces.api.dependencies.cache.RedisCache.delete_pattern", new_callable=AsyncMock, return_value=1),
        patch("src.interfaces.api.dependencies.tasks.CeleryTaskQueue.send_task", new_callable=AsyncMock, return_value=str(uuid.uuid4())),
        patch("src.interfaces.api.dependencies.tasks.CeleryTaskQueue.get_result", new_callable=AsyncMock, return_value=None),
    ):
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test"
        ) as client:
            yield client

    db_manager._async_session_maker = original_factory
    db_manager._engine = original_engine


class TestCarsAPI:
    async def test_health_check(self, async_client):
        response = await async_client.get("/health")
        assert response.status_code == 200

    async def test_create_car(self, async_client):
        payload = {"brand": "BMW", "model": "X5", "year": 2024, "price": 50000}
        response = await async_client.post("/cars/", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["brand"] == "BMW"

    async def test_get_all_cars(self, async_client):
        await async_client.post(
            "/cars/", json={"brand": "BMW", "model": "X5", "year": 2024, "price": 50000}
        )
        response = await async_client.get("/cars/")
        assert response.status_code == 200
        assert len(response.json()) >= 1

    async def test_get_car_not_found(self, async_client):
        response = await async_client.get(f"/cars/{uuid.uuid4()}")
        assert response.status_code == 404

    async def test_update_car(self, async_client):
        create_resp = await async_client.post(
            "/cars/", json={"brand": "BMW", "model": "X5", "year": 2024, "price": 50000}
        )
        car_id = create_resp.json()["id"]

        update_resp = await async_client.put(
            f"/cars/{car_id}",
            json={"brand": "Audi", "model": "A4", "year": 2023, "price": 40000},
        )
        assert update_resp.status_code == 200
        assert update_resp.json()["brand"] == "Audi"

    async def test_delete_car(self, async_client):
        create_resp = await async_client.post(
            "/cars/", json={"brand": "BMW", "model": "X5", "year": 2024, "price": 50000}
        )
        car_id = create_resp.json()["id"]

        delete_resp = await async_client.delete(f"/cars/{car_id}")
        assert delete_resp.status_code == 204

        get_resp = await async_client.get(f"/cars/{car_id}")
        assert get_resp.status_code == 404