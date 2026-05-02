from src.interfaces.api.dependencies.database import get_db_session
from src.interfaces.api.dependencies.services import get_car_service

__all__ = ["get_car_service", "get_db_session"]
