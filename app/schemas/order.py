from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.base import PaginatedResponse


class OrderItemCreate(BaseModel):
    item_id: UUID
    quantity: int = Field(..., ge=1)


class OrderItemResponse(BaseModel):
    id: UUID
    item_id: UUID
    price: Decimal
    quantity: int
    total: Decimal

    model_config = ConfigDict(from_attributes=True)


class OrderCreate(BaseModel):
    items: list[OrderItemCreate]


class OrderUpdate(BaseModel):
    items: list[OrderItemCreate]


class OrderResponse(BaseModel):
    id: UUID
    user_id: UUID
    is_closed: bool
    cost: Decimal
    items: list[OrderItemResponse]

    model_config = ConfigDict(from_attributes=True)


class OrderListResponse(PaginatedResponse[OrderResponse]):
    pass
