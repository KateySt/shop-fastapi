from abc import ABC, abstractmethod
from uuid import UUID

from app.dependencies import CompanyFilters, PaginationParams, SortingParams
from app.schemas.item import ItemCreate, ItemListResponse, ItemResponse, ItemUpdate


class AbstractItemService(ABC):

    @abstractmethod
    async def create_item(self, data: ItemCreate) -> ItemResponse: ...

    @abstractmethod
    async def get_item(self, item_id: UUID) -> ItemResponse: ...

    @abstractmethod
    async def list_items(
        self,
        pagination: PaginationParams,
        sort: SortingParams,
        filters: CompanyFilters,
    ) -> ItemListResponse: ...

    @abstractmethod
    async def update_item(self, item_id: UUID, data: ItemUpdate) -> ItemResponse: ...

    @abstractmethod
    async def delete_item(self, item_id: UUID) -> None: ...
