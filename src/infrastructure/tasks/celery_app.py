from celery import Celery
from kombu import Queue

from src.infrastructure.config.settings import settings

celery_app = Celery(
    "default_redis_cache",
    broker=str(settings.CELERY_BROKER_URL),
    backend=str(settings.CELERY_BACKEND_URL),
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",

    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    result_expires=120,

    task_default_exchange="default_redis_cache",
    task_default_exchange_type="topic",
    task_default_queue="default",
    task_default_routing_key="task.default",
    task_queues=(
        Queue(
            "default",
            routing_key="task.default",
        ),
        Queue(
            "cars",
            routing_key="task.car",
        ),
    ),
    task_routes={
        "car_tasks.*": {
            "queue": "cars",
            "routing_key": "task.car",
        },
    },
    task_reject_on_worker_lost=True,
    imports=("src.infrastructure.tasks.car_tasks",),
)

celery_app.autodiscover_tasks([
    "src.infrastructure.tasks",
])
