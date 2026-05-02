from abc import ABC, abstractmethod
from typing import Any


class CacheInterface(ABC):
    @abstractmethod
    async def get(self, key: str) -> Any | None:
        pass

    @abstractmethod
    async def set(self, key: str, value: Any, ttl: int | None = None) -> bool:
        pass

    @abstractmethod
    async def delete(self, *keys: str) -> int:
        pass

    @abstractmethod
    async def delete_pattern(self, pattern: str) -> int:
        pass
