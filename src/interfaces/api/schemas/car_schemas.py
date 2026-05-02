import uuid
from datetime import datetime
from pydantic import BaseModel, Field, field_validator


class CarCreateSchema(BaseModel):
    brand: str = Field(min_length=1, max_length=100)
    model: str = Field(min_length=1, max_length=100)
    year: int = Field(ge=1886, le=2100)
    price: int = Field(gt=0)

    @field_validator('brand', 'model')
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('Field cannot be empty')
        return v.strip()


class CarUpdateSchema(BaseModel):
    brand: str | None = Field(None, min_length=1, max_length=100)
    model: str | None = Field(None, min_length=1, max_length=100)
    year: int | None = Field(None, ge=1886, le=2100)
    price: int | None = Field(None, gt=0)


class CarResponseSchema(BaseModel):
    id: uuid.UUID
    brand: str
    model: str
    year: int
    price: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
