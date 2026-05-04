from typing import Callable, Awaitable

from src.domain.interfaces.event_consumer import EventConsumerInterface
from src.infrastructure.messaging.kafka_consumer_client import kafka_consumer_client


class KafkaEventConsumer(EventConsumerInterface):
    def __init__(self):
        self._kafka = kafka_consumer_client

    async def subscribe(self, topic: str, handler: Callable[[dict], Awaitable[None]]) -> None:
        await self._kafka.subscribe(topic, handler)
