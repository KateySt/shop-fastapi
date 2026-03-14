from typing import Any

from app.db.models.item import Item
from app.mappers.base_mapper import BaseMapper
from app.mappers.paginated_mapper import PaginatedMapper
from app.schemas.item import ItemCreate, ItemUpdate, ItemResponse, ItemListResponse


class ItemMapper(
    BaseMapper[
        Item,
        ItemCreate,
        ItemUpdate,
        ItemResponse
    ]
):
    def __init__(self):
        super().__init__(
            orm_class=Item,
            response_class=ItemResponse,
        )

    def from_create(self, dto: ItemCreate, **extra: Any) -> Item:
        data = dto.model_dump()
        data.update(extra)
        return Item(**data)


class ItemPaginatedMapper(PaginatedMapper[Item, ItemListResponse]):
    def __init__(self):
        super().__init__(
            orm_class=Item,
            response_class=ItemListResponse,
            item_schema=ItemResponse,
        )
