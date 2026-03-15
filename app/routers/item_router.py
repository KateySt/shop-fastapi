from uuid import UUID

from fastapi import APIRouter, status

from app.dependencies import CompanyFiltersDep, Pagination, Sorting
from app.schemas.item import ItemCreate, ItemListResponse, ItemResponse, ItemUpdate
from app.services import ItemServiceDep

router = APIRouter()


@router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item(
    data: ItemCreate,
    service: ItemServiceDep,
):
    return await service.create_item(data)


@router.get("/{item_id}", response_model=ItemResponse)
async def get_item(
    item_id: UUID,
    service: ItemServiceDep,
):
    return await service.get_item(item_id)


@router.get("/", response_model=ItemListResponse)
async def list_items(
    service: ItemServiceDep,
    pagination: Pagination,
    sort: Sorting,
    filters: CompanyFiltersDep,
):
    return await service.list_items(pagination, sort, filters)


@router.patch("/{item_id}", response_model=ItemResponse)
async def update_item(
    item_id: UUID,
    data: ItemUpdate,
    service: ItemServiceDep,
):
    return await service.update_item(item_id, data)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(
    item_id: UUID,
    service: ItemServiceDep,
):
    await service.delete_item(item_id)
