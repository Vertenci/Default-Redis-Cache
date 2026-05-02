import uuid
from datetime import datetime

from sqlalchemy import UUID, String, Integer, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.database.base import Base


class CarModel(Base):
    __tablename__ = 'cars'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    brand: Mapped[str] = mapped_column(
        String(100),
    )

    model: Mapped[str] = mapped_column(
        String(100),
    )

    year: Mapped[int] = mapped_column(
        Integer,
    )

    price: Mapped[int] = mapped_column(
        Integer
    )

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
