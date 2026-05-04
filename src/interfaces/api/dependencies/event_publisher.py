from src.domain.interfaces.event_publisher import EventPublisherInterface
from src.infrastructure.messaging.kafka_event_publisher import KafkaEventPublisher


async def get_event_publisher() -> EventPublisherInterface:
    return KafkaEventPublisher()
