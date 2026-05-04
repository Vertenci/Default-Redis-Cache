import json

from aiokafka import AIOKafkaProducer

from src.infrastructure.config.settings import settings


class KafkaProducerClient:
    def __init__(self):
        self._producer: AIOKafkaProducer | None = None

    async def initialize(self):
        try:
            self._producer = AIOKafkaProducer(
                bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
                value_serializer=lambda v: json.dumps(v, default=str).encode('utf-8'),
                key_serializer=lambda k: k.encode('utf-8') if k else None,
            )
            await self._producer.start()
        except Exception:
            raise

    async def close(self):
        if self._producer:
            await self._producer.stop()
            self._producer = None

    async def send(self, topic: str, key: str, value: dict) -> None:
        await self._producer.send_and_wait(topic=topic, key=key, value=value)


kafka_producer_client = KafkaProducerClient()
