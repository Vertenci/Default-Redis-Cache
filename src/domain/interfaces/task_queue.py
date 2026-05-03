from abc import ABC, abstractmethod
from typing import Any


class TaskQueueInterface(ABC):
    @abstractmethod
    async def send_task(self, task_name: str, *args, **kwargs) -> str:
        pass

    @abstractmethod
    async def get_result(self, task_id: str) -> Any | None:
        pass
