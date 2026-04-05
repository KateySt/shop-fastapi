from uuid import UUID

from fastapi import UploadFile

from app.dependencies import CompanyFilters, PaginationParams, SortingParams
from app.mappers.item_mapper import ItemMapper, ItemPaginatedMapper
from app.schemas.item import ItemCreate, ItemListResponse, ItemResponse, ItemUpdate
from app.services.abstract.abstract_item_service import AbstractItemService
from app.services.impl.item_service_impl import ItemServiceImpl


class ItemService(AbstractItemService):
    def __init__(
        self,
        impl: ItemServiceImpl,
        mapper: ItemMapper,
        paginated_mapper: ItemPaginatedMapper,
    ):
        self.impl = impl
        self.mapper = mapper
        self.paginated_mapper = paginated_mapper

    async def create_item(self, data: ItemCreate) -> ItemResponse:
        orm = await self.impl.create_item(self.mapper.from_create(data))
        return self.mapper.to_response(orm)

    async def get_item(self, item_id: UUID) -> ItemResponse:
        orm = await self.impl.get_item(item_id)
        return self.mapper.to_response(orm)

    async def list_items(
        self,
        pagination: PaginationParams,
        sort: SortingParams,
        filters: CompanyFilters,
    ) -> ItemListResponse:
        items, total = await self.impl.list_items(
            pagination,
            sort,
            filters,
        )
        return self.paginated_mapper.from_orm_list(
            orm_list=items, total=total, pagination=pagination
        )

    async def update_item(self, item_id: UUID, data: ItemUpdate) -> ItemResponse:
        orm = await self.impl.update_item(item_id, self.mapper.from_update(data))
        return self.mapper.to_response(orm)

    async def delete_item(self, item_id: UUID) -> None:
        await self.impl.delete_item(item_id)

    async def upload_image(self, item_id: UUID, file: UploadFile) -> ItemResponse:
        return self.mapper.to_response(await self.impl.upload_image(item_id, file))

    async def delete_image(self, item_id: UUID, url_to_delete: str) -> ItemResponse:
        return self.mapper.to_response(
            await self.impl.delete_image(item_id, url_to_delete)
        )
