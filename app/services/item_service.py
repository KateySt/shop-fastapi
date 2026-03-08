from uuid import UUID

from app.mappers.item_mapper import ItemMapper, ItemPaginatedMapper
from app.schemas.item import ItemCreate, ItemUpdate, ItemResponse, ItemListResponse
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
        orm = await self.impl.create_item(
            self.mapper.from_create(data)
        )
        return self.mapper.to_response(orm)

    async def get_item(self, item_id: UUID) -> ItemResponse:
        orm = await self.impl.get_item(item_id)
        return self.mapper.to_response(orm)

    async def list_items(
            self,
            skip: int = 0,
            limit: int = 20,
            company_id: UUID | None = None,
            visible: bool | None = None,
    ) -> ItemListResponse:
        items, total = await self.impl.list_items(
            skip=skip, limit=limit,
            company_id=company_id, visible=visible
        )
        return self.paginated_mapper.from_orm_list(
            orm_list=items, total=total, skip=skip, limit=limit
        )

    async def update_item(self, item_id: UUID, data: ItemUpdate) -> ItemResponse:
        orm = await self.impl.update_item(
            item_id, self.mapper.from_update(data)
        )
        return self.mapper.to_response(orm)

    async def delete_item(self, item_id: UUID) -> None:
        await self.impl.delete_item(item_id)
