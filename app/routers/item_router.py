import uuid

from fastapi import APIRouter, Depends, status, Query

from app.schemas import ItemCreate, ItemBase, ItemListResponse
from app.services import ItemService, get_item_service

router = APIRouter()


@router.post("/", response_model=ItemBase, status_code=status.HTTP_201_CREATED)
async def create_item(
        item_data: ItemCreate,
        service: ItemService = Depends(get_item_service)
):
    return await service.create_item(item_data)


@router.get("/{item_id}", response_model=ItemBase)
async def get_item(
        item_id: uuid.UUID,
        service: ItemService = Depends(get_item_service)
):
    return ItemBase.model_validate(await service.get_item(item_id))


@router.get("/", response_model=ItemListResponse)
async def list_items(
        skip: int = Query(0, ge=0),
        limit: int = Query(20, ge=1, le=100),
        company_id: uuid.UUID | None = Query(None),
        visible: bool | None = Query(None),
        service: ItemService = Depends(get_item_service)
):
    return await service.list_items(skip=skip, limit=limit, company_id=company_id, visible=visible)


@router.put("/", response_model=ItemBase)
async def update_item(
        item: ItemBase,
        service: ItemService = Depends(get_item_service)
):
    return await service.update_item(item)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(
        item_id: uuid.UUID,
        service: ItemService = Depends(get_item_service)
):
    await service.delete_item(item_id)
