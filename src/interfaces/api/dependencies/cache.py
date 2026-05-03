from src.domain.interfaces.cache import CacheInterface
from src.infrastructure.cache.redis_cache import RedisCache


async def get_cache() -> CacheInterface:
    return RedisCache()
