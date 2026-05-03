import time
import logging

from celery import shared_task

logger = logging.getLogger(__name__)

@shared_task(
    name="car_tasks.send_car_created_notification",
    bind=True,
    max_retries=3,
    retry_jitter=True,
    acks_late=True
)
def send_car_created_notification(self, car_id: str, brand: str, model: str, email: str = "admin@example.com"):

    logger.info(
        f"Task {self.request.id}: Sending notification "
        f"for car {car_id} ({brand} {model}) to {email}"
    )

    try:
        time.sleep(1)

        result = f"Notification sent to {email} for car {brand} {model}"
        logger.info(f"Task {self.request.id}: {result}")
        return result
    except Exception as exc:
        logger.error(f"Task {self.request.id} failed: {exc}")
        raise self.retry(exc=exc, countdown=60)
