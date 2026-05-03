from typing import Annotated

from pydantic import PostgresDsn, RedisDsn, AmqpDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: Annotated[PostgresDsn, "Async SQLAlchemy DSN"]
    POSTGRES_USER: Annotated[str, "PostgreSQL user"]
    POSTGRES_PASSWORD: Annotated[str, "PostgreSQL password"]
    POSTGRES_DB: Annotated[str, "PostgreSQL database name"]

    REDIS_URL: RedisDsn = "redis://redis:6379/0"
    CELERY_BACKEND_URL: RedisDsn = "redis://redis:6379/1"
    CELERY_BROKER_URL: AmqpDsn = "amqp://guest:guest@rabbitmq:5672//"


settings = Settings()
