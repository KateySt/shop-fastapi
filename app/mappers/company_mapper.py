from typing import Any

from app.db.models import Company
from app.mappers.base_mapper import BaseMapper
from app.mappers.paginated_mapper import PaginatedMapper
from app.schemas import (
    CompanyCreate,
    CompanyListResponse,
    CompanyResponse,
    CompanyUpdate,
)


class CompanyMapper(BaseMapper[Company, CompanyCreate, CompanyUpdate, CompanyResponse]):
    def __init__(self):
        super().__init__(
            orm_class=Company,
            response_class=CompanyResponse,
        )

    def from_create(self, dto: CompanyCreate, **extra: Any) -> Company:
        data = dto.model_dump()
        data.update(extra)
        return Company(**data)


class CompanyPaginatedMapper(PaginatedMapper[Company, CompanyListResponse]):
    def __init__(self):
        super().__init__(
            orm_class=Company,
            response_class=CompanyListResponse,
            item_schema=CompanyResponse,
        )
