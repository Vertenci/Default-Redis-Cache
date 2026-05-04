from src.domain.interfaces.event_publisher import EventPublisherInterface
from src.infrastructure.messaging.kafka_producer_client import kafka_producer_client


class KafkaEventPublisher(EventPublisherInterface):
    def __init__(self):
        self._kafka = kafka_producer_client

    async def publish(self, topic: str, key: str, value: dict) -> None:
        await self._kafka.send(topic, key, value)
