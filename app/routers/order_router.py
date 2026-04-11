from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.db.models import User
from app.dependencies import Pagination, Sorting
from app.dependencies.auth import get_current_user
from app.schemas.order import OrderCreate, OrderListResponse, OrderResponse, OrderUpdate
from app.services import OrderServiceDep

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(
    data: OrderCreate,
    service: OrderServiceDep,
    user: User = Depends(get_current_user),
):
    return await service.create_order(user, data)


@router.get("/", response_model=OrderListResponse)
async def list_orders(
    service: OrderServiceDep,
    pagination: Pagination,
    sort: Sorting,
    user: User = Depends(get_current_user),
):
    return await service.list_orders(user, pagination, sort)


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: UUID,
    service: OrderServiceDep,
    user: User = Depends(get_current_user),
):
    return await service.get_order(order_id, user)


@router.patch("/{order_id}", response_model=OrderResponse)
async def update_order(
    order_id: UUID,
    data: OrderUpdate,
    service: OrderServiceDep,
    user: User = Depends(get_current_user),
):
    return await service.update_order(order_id, user, data)


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(
    order_id: UUID,
    service: OrderServiceDep,
    user: User = Depends(get_current_user),
):
    await service.delete_order(order_id, user)


@router.post("/{order_id}/close", response_model=OrderResponse)
async def close_order(
    order_id: UUID,
    service: OrderServiceDep,
    user: User = Depends(get_current_user),
):
    return await service.close_order(order_id, user)
