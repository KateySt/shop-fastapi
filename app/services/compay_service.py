from app.db.models import Company
from app.exception import NotFoundError
from app.repo import CompanyRepository
from app.schemas import CompanyCreate, CompanyBase, CompanyListResponse


class CompanyService:
    def __init__(self, repo: CompanyRepository):
        self.repo = repo

    async def create_company(self, company_data: CompanyCreate) -> CompanyBase:
        company = await self.repo.add(
            Company(**company_data.model_dump())
        )
        return CompanyBase.model_validate(company)

    async def get_company(self, company_id) -> Company:
        company = await self.repo.get(company_id)
        if not company:
            raise NotFoundError("Company not found")
        return company

    async def list_companies(self, skip=0, limit=20) -> CompanyListResponse:
        companies = await self.repo.list(skip=skip, limit=limit)
        total = await self.repo.count_all()
        company_list = [CompanyBase.model_validate(company) for company in companies]
        return CompanyListResponse(items=company_list, total=total)

    async def update_company(self, company: CompanyBase) -> CompanyBase:
        existing_company = await self.get_company(company.id)
        updated_company = await self.repo.update(existing_company, company.model_dump(exclude_unset=True))
        return CompanyBase.model_validate(updated_company)

    async def delete_company(self, company_id):
        company = await self.get_company(company_id)
        await self.repo.delete(company)
        return True
