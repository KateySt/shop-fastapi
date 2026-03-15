from uuid import UUID

from fastapi import APIRouter, Query, status

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
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    company_id: UUID | None = Query(None),
    visible: bool | None = Query(None),
):
    return await service.list_items(
        skip=skip, limit=limit, company_id=company_id, visible=visible
    )


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
