from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.schemas import PaginatedResponse


class CompanyBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    description: str = Field(..., min_length=3, max_length=255)
    visible: bool

    model_config = ConfigDict(from_attributes=True)


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(BaseModel):
    name: str | None = Field(None, min_length=3, max_length=100)
    description: str | None = Field(None, min_length=3, max_length=255)
    visible: bool | None = None


class CompanyResponse(CompanyBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)


class CompanyListResponse(PaginatedResponse[CompanyResponse]):
    pass
