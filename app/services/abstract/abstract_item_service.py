from abc import ABC, abstractmethod
from uuid import UUID

from app.schemas.item import ItemCreate, ItemUpdate, ItemResponse, ItemListResponse


class AbstractItemService(ABC):

    @abstractmethod
    async def create_item(self, data: ItemCreate) -> ItemResponse: ...

    @abstractmethod
    async def get_item(self, item_id: UUID) -> ItemResponse: ...

    @abstractmethod
    async def list_items(
            self,
            skip: int,
            limit: int,
            company_id: UUID | None,
            visible: bool | None,
    ) -> ItemListResponse: ...

    @abstractmethod
    async def update_item(
            self, item_id: UUID, data: ItemUpdate
    ) -> ItemResponse: ...

    @abstractmethod
    async def delete_item(self, item_id: UUID) -> None: ...
