from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.db.models import User
from app.db.models.enums import UserPermissionsEnum
from app.dependencies.auth import get_admin_user, get_current_user, require_permissions
from app.schemas.user import CreateUserSchema, UpdateUserSchema, UserResponseSchema
from app.services import UserServiceDep

router = APIRouter()


@router.post(
    "/",
    response_model=UserResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    data: CreateUserSchema,
    service: UserServiceDep,
):
    return await service.create_user(data)


@router.get(
    "/me",
    response_model=UserResponseSchema,
)
async def get_me(
    current_user: User = Depends(get_current_user),
):
    return current_user


@router.patch(
    "/me",
    response_model=UserResponseSchema,
)
async def update_me(
    data: UpdateUserSchema,
    service: UserServiceDep,
    current_user: User = Depends(get_current_user),
):
    return await service.update_user(current_user.id, data)


@router.delete(
    "/me",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_me(
    service: UserServiceDep,
    current_user: User = Depends(
        require_permissions([UserPermissionsEnum.CAN_SELF_DELETE])
    ),
):
    await service.delete_user(current_user.id)


@router.get(
    "/{user_id}",
    response_model=UserResponseSchema,
    dependencies=[Depends(get_admin_user)],
)
async def get_user(
    user_id: UUID,
    service: UserServiceDep,
):
    return await service.get_user(user_id)


@router.patch(
    "/{user_id}",
    response_model=UserResponseSchema,
    dependencies=[Depends(get_admin_user)],
)
async def update_user(
    user_id: UUID,
    data: UpdateUserSchema,
    service: UserServiceDep,
):
    return await service.update_user(user_id, data)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_admin_user)],
)
async def delete_user(
    user_id: UUID,
    service: UserServiceDep,
):
    await service.delete_user(user_id)
