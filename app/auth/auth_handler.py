import datetime
from uuid import uuid4

import jwt
from fastapi.security import OAuth2PasswordRequestForm

from ..config import auth_config
from ..db.models import User
from ..exception import ForbiddenError, UnauthorizedError, ValidationError
from ..schemas.user import LoginResponseSchema
from ..services import RedisService
from .password_handler import PasswordEncrypt


class AuthHandler:
    def __init__(self, redis: RedisService):
        self.access_token_lifetime = auth_config.ACCESS_TOKEN_TIME_MINUTES
        self.refresh_token_lifetime = auth_config.REFRESH_TOKEN_TIME_MINUTES
        self.jwt_algorithm = auth_config.JWT_ALGORITHM
        self.jwt_secret = auth_config.JWT_SECRET
        self.redis = redis

    async def get_login_token_pairs(
        self, user: User, data: OAuth2PasswordRequestForm
    ) -> LoginResponseSchema:
        is_valid_password = PasswordEncrypt.verify_password(
            plain_password=data.password,
            hashed_password=user.hashed_password,
        )
        if not is_valid_password:
            raise ForbiddenError(detail="Incorrect password")
        return await self.generate_tokens(user)

    async def generate_tokens(self, user: User) -> LoginResponseSchema:
        access_token_payload = {
            "sub": str(user.id),
            "email": user.email,
        }
        access_token = await self.generate_token(
            access_token_payload, self.access_token_lifetime
        )

        token_key = uuid4().hex
        refresh_token_payload = {
            "sub": str(user.id),
            "email": user.email,
            "key": token_key,
        }
        refresh_token = await self.generate_token(
            refresh_token_payload, self.refresh_token_lifetime
        )

        await self.redis.set_cache(
            key=token_key,
            value=str(user.id),
            ttl=self.refresh_token_lifetime * 60,
        )
        return LoginResponseSchema(
            access_token=access_token,
            refresh_token=refresh_token,
            expired_at=self.access_token_lifetime * 60,
        )

    async def generate_token(self, payload: dict, expire_minutes: int) -> str:
        now = datetime.datetime.now(datetime.UTC)
        payload = payload.copy()
        payload.update(
            {
                "exp": now + datetime.timedelta(minutes=expire_minutes),
                "iat": now,
            }
        )
        return jwt.encode(payload, self.jwt_secret, self.jwt_algorithm)

    async def decode_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, self.jwt_secret, [self.jwt_algorithm])
            payload["iat"] = datetime.datetime.fromtimestamp(
                payload.get("iat") or 0,
                tz=datetime.UTC,
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise UnauthorizedError(detail="Token expired")
        except jwt.InvalidTokenError:
            raise ValidationError(detail="Invalid token")

    async def get_refresh_token_pair(
        self, refresh_token: str, user: User
    ) -> LoginResponseSchema:
        payload = await self.decode_token(refresh_token)

        token_key = payload.get("key")
        if not token_key:
            raise UnauthorizedError(
                detail="Access token was provided instead of refresh"
            )

        if str(user.id) != payload["sub"]:
            raise UnauthorizedError(detail="Token does not belong to this user")

        stored = await self.redis.get_cache(token_key)
        if not stored:
            raise UnauthorizedError(detail="Refresh token already used or expired")

        await self.redis.delete_cache(token_key)

        if user.use_token_since and user.use_token_since > payload["iat"]:
            raise UnauthorizedError(detail="User was force logged out")

        return await self.generate_tokens(user)
