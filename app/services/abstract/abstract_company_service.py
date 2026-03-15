from abc import ABC, abstractmethod
from uuid import UUID

from app.schemas import (
    CompanyCreate,
    CompanyListResponse,
    CompanyResponse,
    CompanyUpdate,
)


class AbstractCompanyService(ABC):
    @abstractmethod
    async def create_company(self, data: CompanyCreate) -> CompanyResponse: ...

    @abstractmethod
    async def get_company(self, company_id: UUID) -> CompanyResponse: ...

    @abstractmethod
    async def list_companies(self, skip: int, limit: int) -> CompanyListResponse: ...

    @abstractmethod
    async def update_company(
        self, company_id: UUID, data: CompanyUpdate
    ) -> CompanyResponse: ...

    @abstractmethod
    async def delete_company(self, company_id: UUID) -> None: ...
