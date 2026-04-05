from uuid import UUID

from fastapi import UploadFile

from app.db.models.item import Item
from app.dependencies import CompanyFilters, PaginationParams, SortingParams
from app.exception import NotFoundError
from app.repo.item_repository import ItemRepository
from app.storage import s3_storage


class ItemServiceImpl:
    def __init__(self, repo: ItemRepository):
        self.repo = repo

    async def create_item(self, item: Item) -> Item:
        await self.repo.add(item)
        return item

    async def get_item(self, item_id: UUID) -> Item:
        item = await self.repo.get(item_id)
        if not item:
            raise NotFoundError("Item not found")
        return item

    async def list_items(
        self,
        pagination: PaginationParams,
        sort: SortingParams,
        filters: CompanyFilters,
    ) -> tuple[list[Item], int]:
        items = await self.repo.list(
            **pagination.to_dict(), **sort.to_dict(), **filters.to_dict()
        )
        total = await self.repo.count_all(**filters.to_dict())
        return list(items), total

    async def update_item(self, item_id: UUID, data: dict) -> Item:
        item = await self.get_item(item_id)
        updated = await self.repo.update(item, data)
        return updated

    async def delete_item(self, item_id: UUID) -> None:
        item = await self.get_item(item_id)

        if item.images:
            for url in item.images:
                await s3_storage.delete_file(url)

        await self.repo.delete(item)

    async def upload_image(self, item_id: UUID, file: UploadFile) -> Item:
        item = await self.get_item(item_id)

        new_url = await s3_storage.upload_file(
            file=file,
            uuid_obj=item_id,
            root_dir="images",
        )

        updated_images = list(item.images or []) + [new_url]
        return await self.update_item(item_id, {"images": updated_images})

    async def delete_image(self, item_id: UUID, url_to_delete: str) -> Item:
        item = await self.get_item(item_id)

        await s3_storage.delete_file(url_to_delete)

        remaining = [url for url in (item.images or []) if url != url_to_delete]
        return await self.update_item(item_id, {"images": remaining})
