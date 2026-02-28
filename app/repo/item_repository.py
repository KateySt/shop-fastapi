from app.db.models import Item
from app.repo.base_repository import BaseRepository


class ItemRepository(BaseRepository[Item]):
    def __init__(self, session):
        super().__init__(session, Item)
