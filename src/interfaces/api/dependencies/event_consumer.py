from src.domain.interfaces.event_consumer import EventConsumerInterface
from src.infrastructure.messaging.kafka_event_consumer import KafkaEventConsumer


async def get_event_consumer() -> EventConsumerInterface:
    return KafkaEventConsumer()
