from uuid import UUID

from app.db.models.item import Item
from app.exception import NotFoundError
from app.repo.item_repository import ItemRepository


class ItemServiceImpl:
    def __init__(self, repo: ItemRepository):
        self.repo = repo

    async def create_item(self, item: Item) -> Item:
        await self.repo.add(item)
        await self.repo.commit()
        return item

    async def get_item(self, item_id: UUID) -> Item:
        item = await self.repo.get(item_id)
        if not item:
            raise NotFoundError("Item not found")
        return item

    async def list_items(
            self,
            skip: int = 0,
            limit: int = 20,
            company_id: UUID | None = None,
            visible: bool | None = None,
    ) -> tuple[list[Item], int]:
        items = await self.repo.list(
            skip=skip, limit=limit,
            company_id=company_id, visible=visible
        )
        total = await self.repo.count_all(
            company_id=company_id, visible=visible
        )
        return list(items), total

    async def update_item(self, item_id: UUID, data: dict) -> Item:
        item = await self.get_item(item_id)
        updated = await self.repo.update(item, data)
        await self.repo.commit()
        return updated

    async def delete_item(self, item_id: UUID) -> None:
        item = await self.get_item(item_id)
        await self.repo.delete(item)
        await self.repo.commit()
