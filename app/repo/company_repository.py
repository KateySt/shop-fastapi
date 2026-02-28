from app.db.models import Company
from app.repo.base_repository import BaseRepository


class CompanyRepository(BaseRepository[Company]):
    def __init__(self, session):
        super().__init__(session, Company)
