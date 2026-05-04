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

    @abstractmethod
    async def increment(self, key: str, amount: int = 1) -> int:
        pass

    @abstractmethod
    async def get_keys_by_pattern(self, pattern: str) -> list[str]:
        pass

    @abstractmethod
    async def lpush(self, key: str, *values: str) -> int:
        pass

    @abstractmethod
    async def ltrim(self, key: str, start: int, end: int) -> bool:
        pass

    @abstractmethod
    async def lrange(self, key: str, start: int, end: int) -> list:
        pass
