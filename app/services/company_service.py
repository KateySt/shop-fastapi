from uuid import UUID

from app.mappers import CompanyMapper, CompanyPaginatedMapper
from app.schemas import (
    CompanyCreate, CompanyUpdate,
    CompanyResponse, CompanyListResponse
)
from app.services.abstract.abstract_company_service import AbstractCompanyService
from app.services.impl import CompanyServiceImpl


class CompanyService(AbstractCompanyService):
    def __init__(
            self,
            impl: CompanyServiceImpl,
            mapper: CompanyMapper,
            paginated_mapper: CompanyPaginatedMapper,
    ):
        self.impl = impl
        self.mapper = mapper
        self.paginated_mapper = paginated_mapper

    async def create_company(
            self, data: CompanyCreate
    ) -> CompanyResponse:
        orm = await self.impl.create_company(
            self.mapper.from_create(data)
        )
        return self.mapper.to_response(orm)

    async def get_company(
            self, company_id: UUID
    ) -> CompanyResponse:
        orm = await self.impl.get_company(company_id)
        return self.mapper.to_response(orm)

    async def list_companies(
            self, skip: int = 0, limit: int = 20
    ) -> CompanyListResponse:
        companies, total = await self.impl.list_companies(skip, limit)
        return self.paginated_mapper.from_orm_list(
            orm_list=companies,
            total=total,
            skip=skip,
            limit=limit,
        )

    async def update_company(
            self, company_id: UUID, data: CompanyUpdate
    ) -> CompanyResponse:
        orm = await self.impl.update_company(
            company_id,
            self.mapper.from_update(data)
        )
        return self.mapper.to_response(orm)

    async def delete_company(self, company_id: UUID) -> None:
        await self.impl.delete_company(company_id)
