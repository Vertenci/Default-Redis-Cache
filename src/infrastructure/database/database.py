import logging
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine, AsyncSession
from ..config.settings import settings


class DatabaseManager:
    def __init__(self):
        self._engine: AsyncEngine | None = None
        self._async_session_maker: async_sessionmaker | None = None

    async def initialize(self):
        self._engine = create_async_engine(
            str(settings.DATABASE_URL),
            echo=False,
            pool_pre_ping=True,
        )

        self._async_session_maker = async_sessionmaker(
            self._engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=False,
        )

    async def close(self):
        if self._engine:
            await self._engine.dispose()

    def get_session_factory(self) -> async_sessionmaker:
        if not self._async_session_maker:
            raise RuntimeError("Database not initialized. Call initialize() first.")
        return self._async_session_maker

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        if not self._async_session_maker:
            raise RuntimeError("Database not initialized")

        async with self._async_session_maker() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()


db_manager = DatabaseManager()
