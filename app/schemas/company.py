from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict, TypeAdapter

from app.schemas import PaginatedResponse


class CompanyBase(BaseModel):
    id: UUID
    name: str = Field(..., min_length=3, max_length=100)
    description: str = Field(..., min_length=3, max_length=255)
    visible: bool

    model_config = {"from_attributes": True}


class CompanyCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    description: str = Field(..., min_length=3, max_length=255)
    visible: bool


class CompanyListResponse(PaginatedResponse[CompanyBase]):
    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_orm_list(cls, companies, total: int) -> "CompanyListResponse":
        return cls(
            items=TypeAdapter(list[CompanyBase]).validate_python(companies, from_attributes=True),
            total=total
        )
