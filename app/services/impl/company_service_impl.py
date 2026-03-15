from uuid import UUID

from app.db.models import Company
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
        self, skip: int = 0, limit: int = 20
    ) -> tuple[list[Company], int]:
        companies = await self.repo.list(skip=skip, limit=limit)
        total = await self.repo.count_all()
        return list(companies), total

    async def update_company(self, company_id: UUID, data: dict) -> Company:
        company = await self.get_company(company_id)
        updated = await self.repo.update(company, data)
        return updated

    async def delete_company(self, company_id: UUID) -> None:
        company = await self.get_company(company_id)
        await self.repo.delete(company)
