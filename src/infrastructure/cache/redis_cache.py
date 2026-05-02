from typing import Any

from src.domain.interfaces.cache import CacheInterface
from src.infrastructure.cache.redis_client import redis_client


class RedisCache(CacheInterface):
    def __init__(self):
        self._redis = redis_client

    async def get(self, key: str) -> Any | None:
        return await self._redis.get(key)

    async def set(self, key: str, value: Any, ttl: int | None = None) -> bool:
        return await self._redis.set(key, value, ttl)

    async def delete(self, *keys: str) -> int:
        return await self._redis.delete(*keys)

    async def delete_pattern(self, pattern: str) -> int:
        return await self._redis.delete_pattern(pattern)
