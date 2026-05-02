from typing import Any
from celery.result import AsyncResult

from src.domain.interfaces.task_queue import TaskQueueInterface


class CeleryTaskQueue(TaskQueueInterface):
    def __init__(self, celery_app):
        self._celery_app = celery_app

    async def send_task(self, task_name: str, *args, **kwargs) -> str:
        result = self._celery_app.send_task(
            task_name,
            args=args,
            kwargs=kwargs,
        )
        return result.id

    async def get_result(self, task_id: str) -> Any | None:
        result = AsyncResult(task_id, app=self._celery_app)
        if result.ready():
            if result.successful():
                return result.get()
            else:
                raise result.result
        return None
