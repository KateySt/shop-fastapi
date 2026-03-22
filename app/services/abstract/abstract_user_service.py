from abc import ABC, abstractmethod
from uuid import UUID

from app.schemas import CreateUserSchema, UpdateUserSchema, UserResponseSchema


class AbstractUserService(ABC):

    @abstractmethod
    async def create_user(self, data: CreateUserSchema) -> UserResponseSchema: ...

    @abstractmethod
    async def get_user(self, user_id: UUID) -> UserResponseSchema: ...

    @abstractmethod
    async def get_user_by_email(self, email: str) -> UserResponseSchema: ...

    @abstractmethod
    async def update_user(
        self, user_id: UUID, data: UpdateUserSchema
    ) -> UserResponseSchema: ...

    @abstractmethod
    async def delete_user(self, user_id: UUID) -> None: ...

    @abstractmethod
    async def force_logout(self, user_id: UUID) -> None: ...
