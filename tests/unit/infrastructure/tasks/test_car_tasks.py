from unittest.mock import patch
from src.infrastructure.tasks.car_tasks import send_car_created_notification


class TestCarTasks:
    def test_send_notification_success(self):
        with patch(
            "src.infrastructure.tasks.car_tasks.send_car_created_notification.retry"
        ) as mock_retry:
            result = send_car_created_notification(
                car_id="test-123",
                brand="BMW",
                model="X5",
                email="test@example.com",
            )
            assert "Notification sent to test@example.com" in result
            mock_retry.assert_not_called()

    def test_send_notification_retry_on_error(self):
        pass
