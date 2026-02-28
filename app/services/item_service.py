from app.db.models import Item
from app.exception import NotFoundError
from app.repo import ItemRepository
from app.schemas import ItemCreate, ItemBase, ItemListResponse


class ItemService:
    def __init__(self, repo: ItemRepository):
        self.repo = repo

    async def create_item(self, item_data: ItemCreate) -> ItemBase:
        item = await self.repo.add(
            Item(**item_data.model_dump())
        )
        return ItemBase.model_validate(item)

    async def get_item(self, item_id) -> Item:
        item = await self.repo.get(item_id)
        if not item:
            raise NotFoundError("Item not found")
        return item

    async def list_items(self, skip=0, limit=20, company_id=None, visible=None) -> ItemListResponse:
        items = await self.repo.list(skip=skip, limit=limit, company_id=company_id, visible=visible)
        total = await self.repo.count_all(company_id=company_id, visible=visible)
        item_list = [ItemBase.model_validate(item) for item in items]
        return ItemListResponse(items=item_list, total=total)

    async def update_item(self, item: ItemBase) -> ItemBase:
        existing_item = await self.get_item(item.id)
        updated_item = await self.repo.update(existing_item, item.model_dump(exclude_unset=True))
        return ItemBase.model_validate(updated_item)

    async def delete_item(self, item_id):
        item = await self.get_item(item_id)
        await self.repo.delete(item)
        return True
