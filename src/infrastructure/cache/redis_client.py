import json
from typing import Any

import redis.asyncio as aioredis

from src.infrastructure.config.settings import settings


class RedisClient:
    def __init__(self):
        self._redis: aioredis.Redis | None = None

    async def initialize(self):
        try:
            self._redis = await aioredis.from_url(
                str(settings.REDIS_URL),
                encoding="utf-8",
                decode_responses=True,
            )
            await self._redis.ping()
        except Exception as e:
            raise

    async def close(self):
        if self._redis:
            await self._redis.aclose()
            self._redis = None

    async def get(self, key: str) -> Any | None:
        try:
            value = await self._redis.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            raise

    async def set(self, key: str, value: Any, ttl: int | None = None) -> bool:
        try:
            serialized = json.dumps(value, default=str)
            if ttl:
                await self._redis.setex(key, ttl, serialized)
            else:
                await self._redis.set(key, serialized)
            return True
        except Exception as e:
            return False

    async def delete(self, *keys: str) -> int:
        try:
            return await self._redis.delete(*keys)
        except Exception as e:
            return 0

    async def delete_pattern(self, pattern: str) -> int:
        try:
            cursor = 0
            deleted = 0
            while True:
                cursor, keys = await self._redis.scan(cursor, match=pattern, count=100)
                if keys:
                    deleted += await self._redis.delete(*keys)
                if cursor == 0:
                    break
            return deleted
        except Exception as e:
            return 0

    async def exists(self, key: str) -> bool:
        try:
            return await self._redis.exists(key) > 0
        except Exception as e:
            raise False


redis_client = RedisClient()
