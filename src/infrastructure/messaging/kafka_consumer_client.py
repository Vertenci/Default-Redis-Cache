import asyncio
import json
from typing import Callable, Awaitable

from aiokafka import AIOKafkaConsumer

from src.infrastructure.config.settings import settings


class KafkaConsumerClient:
    def __init__(self):
        self._consumer: AIOKafkaConsumer | None = None
        self._running = False
        self._task: asyncio.Task | None = None
        self._handlers: dict[str, Callable[[dict], Awaitable[None]]] = {}

    async def initialize(self):
        try:
            self._consumer = AIOKafkaConsumer(
                bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
                group_id="car.events.group",
                value_deserializer=lambda v: json.loads(v.decode('utf-8')),
                auto_offset_reset='earliest',
                enable_auto_commit=True,
            )
            await self._consumer.start()
        except Exception:
            raise

    async def close(self):
        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        if self._consumer:
            await self._consumer.stop()
            self._consumer = None

    async def subscribe(self, topic: str, handler: Callable[[dict], Awaitable[None]]) -> None:
        self._handlers[topic] = handler

    async def start_consuming(self):
        if not self._consumer:
            raise RuntimeError("Consumer not initialized")

        topics = list(self._handlers.keys())
        if topics:
            self._consumer.subscribe(topics=topics)

        self._running = True
        self._task = asyncio.create_task(self._consume_loop())

    async def _consume_loop(self):
        try:
            async for message in self._consumer:
                handler = self._handlers.get(message.topic)
                if handler:
                    try:
                        await handler(message.value)
                    except Exception as e:
                        return f"Error handling message: {e}"
        except asyncio.CancelledError:
            pass
        except Exception as e:
            return f"Consumer loop error: {e}"


kafka_consumer_client = KafkaConsumerClient()
