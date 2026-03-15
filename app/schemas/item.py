from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.db.models import Currency
from app.schemas.base import PaginatedResponse


class ItemBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    description: str = Field(..., min_length=3, max_length=255)
    rating: int = Field(..., ge=0, le=5)
    visible: bool
    company_id: UUID
    price: Decimal = Field(..., ge=Decimal("0.00"), decimal_places=2, max_digits=10)
    currency: Currency = Currency.UAH

    model_config = ConfigDict(from_attributes=True)


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    name: str | None = Field(None, min_length=3, max_length=100)
    description: str | None = Field(None, min_length=3, max_length=255)
    rating: int | None = Field(None, ge=0, le=5)
    visible: bool | None = None


class ItemResponse(ItemBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)


class ItemListResponse(PaginatedResponse[ItemResponse]):
    pass
