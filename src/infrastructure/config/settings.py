from typing import Annotated

from pydantic import RedisDsn, AmqpDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: Annotated[str, "Async SQLAlchemy DSN"]
    POSTGRES_USER: Annotated[str, "PostgreSQL user"]
    POSTGRES_PASSWORD: Annotated[str, "PostgreSQL password"]
    POSTGRES_DB: Annotated[str, "PostgreSQL database name"]

    REDIS_URL: RedisDsn = "redis://redis:6379/0"
    CELERY_BACKEND_URL: RedisDsn = "redis://redis:6379/1"
    CELERY_BROKER_URL: AmqpDsn = "amqp://guest:guest@rabbitmq:5672//"

    KAFKA_BOOTSTRAP_SERVERS: str = "kafka:9092"
    KAFKA_CAR_EVENTS_TOPIC: str = "car.events"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="forbid",
    )


settings = Settings()
