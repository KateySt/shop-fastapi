import datetime
from typing import Annotated
from uuid import UUID

from password_strength import PasswordPolicy
from pydantic import BaseModel, EmailStr, Field, StringConstraints, field_validator


class UserPasswordSchema(BaseModel):
    password: str = Field(examples=["HJHJ98nmn+_+"])

    @field_validator("password")
    @classmethod
    def validate_password_complexity(cls, value: str) -> str:
        policy = PasswordPolicy.from_names(length=8, uppercase=1, numbers=1, special=1)
        errors = policy.test(value)
        if not errors:
            return value

        messages = {
            "length": lambda e: f"At least {e.length} characters",
            "uppercase": lambda e: f"At least {e.count} uppercase letter(s)",
            "numbers": lambda e: f"At least {e.count} digit(s)",
            "special": lambda e: f"At least {e.count} special character(s)",
        }
        error_messages = [messages[e.name()](e) for e in errors if e.name() in messages]
        raise ValueError("; ".join(error_messages))


class BaseUserSchema(BaseModel):
    email: EmailStr = Field(description="User email", examples=["example@gmail.com"])
    name: Annotated[
        str,
        StringConstraints(
            pattern=r"^[0-9a-zA-Zа-яА-ЯіІїЇєЄ_.'\- ]+$",
            strip_whitespace=True,
            max_length=50,
            min_length=3,
        ),
    ] = Field(examples=["John Doe"])


class CreateUserSchema(BaseUserSchema, UserPasswordSchema):
    pass


class UpdateUserSchema(BaseUserSchema):
    pass


class UserResponseSchema(BaseUserSchema):
    id: UUID

    model_config = {"from_attributes": True}


class LoginResponseSchema(BaseModel):
    access_token: str
    refresh_token: str
    expired_at: int
    token_type: str = "Bearer"


class ForceLogoutSchema(BaseModel):
    use_token_since: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(datetime.UTC)
    )
