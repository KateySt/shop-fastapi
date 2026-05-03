from collections.abc import Callable
from enum import StrEnum

import jwt
from fastapi import Depends, Query, WebSocket, WebSocketException, status
from fastapi.security import OAuth2PasswordBearer

from app.auth import AuthHandler, get_auth_handler
from app.config import auth_config
from app.db.models import User
from app.exception import ForbiddenError, NotFoundError, UnauthorizedError
from app.repo import get_repo_user
from app.repo.user_repository import UserRepository


class SecurityHandler:
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


async def get_current_user(
    token: str = Depends(SecurityHandler.oauth2_scheme),
    repo: UserRepository = Depends(get_repo_user),
    auth: AuthHandler = Depends(get_auth_handler),
) -> User:
    payload = await auth.decode_token(token)
    user: User | None = await repo.get(payload["sub"])
    if not user:
        raise NotFoundError(detail="User not found")
    if user.use_token_since and user.use_token_since > payload["iat"]:
        raise UnauthorizedError(detail="User forced logout")
    return user


async def get_admin_user(user: User = Depends(get_current_user)) -> User:
    if user.is_admin:
        return user
    raise ForbiddenError(detail="Admin user is required")


def require_permissions(required_permissions: list[StrEnum]) -> Callable:
    async def dependency(user: User = Depends(get_current_user)) -> User:
        if user.is_admin:
            return user
        user_permissions = set(user.permissions)
        required_permissions_set: set[str] = {
            perm.value for perm in required_permissions
        }

        if required_permissions_set.issubset(user_permissions):
            return user

        raise ForbiddenError(
            detail=f"Permissions {', '.join(required_permissions_set)} required"
        )

    return dependency


async def get_ws_user(
    websocket: WebSocket,
    token: str = Query(...),
    user_repo: UserRepository = Depends(get_repo_user),
) -> User:
    try:
        payload = jwt.decode(
            token,
            auth_config.JWT_SECRET,
            algorithms=[auth_config.JWT_ALGORITHM],
        )
        user_id = payload.get("sub")
        if not user_id:
            raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    except jwt.ExpiredSignatureError:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    except jwt.InvalidTokenError:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)

    user = await user_repo.get(user_id)
    if not user:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)

    return user
