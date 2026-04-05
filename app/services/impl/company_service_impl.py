from uuid import UUID

from app.db.models import Company
from app.dependencies import PaginationParams, SortingParams
from app.exception import NotFoundError
from app.repo import CompanyRepository


class CompanyServiceImpl:
    def __init__(self, repo: CompanyRepository):
        self.repo = repo

    async def create_company(self, company: Company) -> Company:
        company = await self.repo.add(company)
        return company

    async def get_company(self, company_id: UUID) -> Company:
        company = await self.repo.get(company_id)
        if not company:
            raise NotFoundError("Company not found")
        return company

    async def list_companies(
        self,
        pagination: PaginationParams,
        sort: SortingParams,
    ) -> tuple[list[Company], int]:
        companies = await self.repo.list(**pagination.to_dict(), **sort.to_dict())
        total = await self.repo.count_all()
        return list(companies), total

    async def update_company(self, company_id: UUID, data: dict) -> Company:
        company = await self.get_company(company_id)
        updated = await self.repo.update(company, data)
        return updated

    async def delete_company(self, company_id: UUID) -> None:
        company = await self.get_company(company_id)
        await self.repo.delete(company)
