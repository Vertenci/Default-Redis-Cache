from src.domain.interfaces.task_queue import TaskQueueInterface
from src.infrastructure.tasks.task_queue_adapter import CeleryTaskQueue


async def get_task_queue() -> TaskQueueInterface:
    return CeleryTaskQueue()
