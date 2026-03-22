from uuid import UUID

from app.db.models import User
from app.exception import NotFoundError
from app.repo import UserRepository


class UserServiceImpl:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def create_user(self, user: User) -> User:
        await self.repo.add(user)
        return user

    async def get_user(self, user_id: UUID) -> User:
        user = await self.repo.get(user_id)
        if not user:
            raise NotFoundError("User not found")
        return user

    async def get_user_by_email(self, email: str) -> User:
        user = await self.repo.get_by_email(email)
        if not user:
            raise NotFoundError("User not found")
        return user

    async def update_user(self, user_id: UUID, data: dict) -> User:
        user = await self.get_user(user_id)
        updated = await self.repo.update(user, data)
        return updated

    async def delete_user(self, user_id: UUID) -> None:
        user = await self.get_user(user_id)
        await self.repo.delete(user)
