from uuid import UUID

from app.mappers import UserMapper
from app.schemas import (
    CreateUserSchema,
    ForceLogoutSchema,
    UpdateUserSchema,
    UserResponseSchema,
)
from app.services.abstract import AbstractUserService
from app.services.impl import UserServiceImpl


class UserService(AbstractUserService):
    def __init__(
        self,
        impl: UserServiceImpl,
        mapper: UserMapper,
    ):
        self.impl = impl
        self.mapper = mapper

    async def create_user(self, data: CreateUserSchema) -> UserResponseSchema:
        orm = await self.impl.create_user(self.mapper.from_create(data))
        return self.mapper.to_response(orm)

    async def get_user(self, user_id: UUID) -> UserResponseSchema:
        orm = await self.impl.get_user(user_id)
        return self.mapper.to_response(orm)

    async def get_user_by_email(self, email: str) -> UserResponseSchema:
        orm = await self.impl.get_user_by_email(email)
        return self.mapper.to_response(orm)

    async def update_user(
        self, user_id: UUID, data: UpdateUserSchema
    ) -> UserResponseSchema:
        orm = await self.impl.update_user(user_id, self.mapper.from_update(data))
        return self.mapper.to_response(orm)

    async def delete_user(self, user_id: UUID) -> None:
        await self.impl.delete_user(user_id)

    async def force_logout(self, user_id: UUID) -> None:
        data = ForceLogoutSchema()
        await self.impl.update_user(user_id, data.model_dump(exclude_unset=False))
