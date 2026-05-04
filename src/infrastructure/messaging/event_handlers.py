from src.application.services.statistics_service import StatisticsService
from src.infrastructure.cache.redis_cache import RedisCache
from src.infrastructure.messaging.kafka_consumer_client import kafka_consumer_client


async def setup_event_handlers():
    cache = RedisCache()
    statistics_service = StatisticsService(cache)

    await kafka_consumer_client.subscribe("car.events", statistics_service.process_event)
