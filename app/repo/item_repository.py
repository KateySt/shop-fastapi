from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Item
from app.repo.base_repository import BaseRepository


class ItemRepository(BaseRepository[Item]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Item)
