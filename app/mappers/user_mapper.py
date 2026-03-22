from app.auth.password_handler import PasswordEncrypt
from app.db.models import User
from app.mappers.base_mapper import BaseMapper
from app.schemas.user import CreateUserSchema, UpdateUserSchema, UserResponseSchema


class UserMapper(
    BaseMapper[User, CreateUserSchema, UpdateUserSchema, UserResponseSchema]
):
    def __init__(self):
        super().__init__(
            orm_class=User,
            response_class=UserResponseSchema,
        )

    def from_create(self, dto: CreateUserSchema, **extra) -> User:
        data = dto.model_dump()

        password = data.pop("password")
        data["hashed_password"] = PasswordEncrypt.get_password_hash(password)

        data.update(extra)
        return self.orm_class(**data)
