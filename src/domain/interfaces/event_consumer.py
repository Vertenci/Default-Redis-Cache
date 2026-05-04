from abc import ABC, abstractmethod
from typing import Callable, Awaitable


class EventConsumerInterface(ABC):
    @abstractmethod
    async def subscribe(self, topic: str, handler: Callable[[dict], Awaitable[None]]) -> None:
        pass
