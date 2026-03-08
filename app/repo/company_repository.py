from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Company
from app.repo.base_repository import BaseRepository


class CompanyRepository(BaseRepository[Company]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Company)
