from functools import lru_cache

from fastapi import Depends

from app.services.redis_service import RedisService

from .auth_handler import AuthHandler
from .password_handler import PasswordEncrypt


@lru_cache
def get_redis_service() -> RedisService:
    return RedisService()


def get_auth_handler(
    redis: RedisService = Depends(get_redis_service),
) -> AuthHandler:
    return AuthHandler(redis=redis)
