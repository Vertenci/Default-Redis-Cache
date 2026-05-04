from abc import ABC, abstractmethod


class EventPublisherInterface(ABC):
    @abstractmethod
    async def publish(self, topic: str, key: str, value: dict) -> None:
        pass
