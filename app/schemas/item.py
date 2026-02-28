from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict, TypeAdapter

from app.schemas import PaginatedResponse


class ItemBase(BaseModel):
    id: UUID
    name: str = Field(..., min_length=3, max_length=100)
    description: str = Field(..., min_length=3, max_length=255)
    rating: int = Field(..., ge=0, le=5)
    visible: bool

    model_config = {"from_attributes": True}


class ItemCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    description: str = Field(..., min_length=3, max_length=255)
    rating: int = Field(..., ge=0, le=5)
    visible: bool
    company_id: UUID


class ItemUpdate(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    description: str = Field(..., min_length=3, max_length=255)
    rating: int = Field(..., ge=0, le=5)
    visible: bool


class ItemListResponse(PaginatedResponse[ItemBase]):
    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_orm_list(cls, items, total: int) -> "ItemListResponse":
        return cls(
            items=TypeAdapter(list[ItemBase]).validate_python(items, from_attributes=True),
            total=total
        )
