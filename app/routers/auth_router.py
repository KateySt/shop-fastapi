from fastapi import APIRouter, Depends, Header, status
from fastapi.security import OAuth2PasswordRequestForm

from app.auth import AuthHandler, get_auth_handler
from app.db.models import User
from app.dependencies.auth import get_current_user
from app.repo import UserRepository, get_repo_user
from app.schemas.user import LoginResponseSchema
from app.services import UserServiceDep

router = APIRouter()


@router.post("/login", response_model=LoginResponseSchema)
async def user_login(
    data: OAuth2PasswordRequestForm = Depends(),
    auth: AuthHandler = Depends(get_auth_handler),
    repo: UserRepository = Depends(get_repo_user),
):
    user: User | None = await repo.get_by_email(data.username)
    if not user:
        from app.exception import NotFoundError

        raise NotFoundError(detail="User not found")
    return await auth.get_login_token_pairs(user, data)


@router.post("/refresh", response_model=LoginResponseSchema)
async def refresh_user_token(
    refresh_token: str = Header(alias="X-Refresh-Token"),
    auth: AuthHandler = Depends(get_auth_handler),
    repo: UserRepository = Depends(get_repo_user),
):
    payload = await auth.decode_token(refresh_token)
    user: User | None = await repo.get(payload["sub"])
    if not user:
        from app.exception import NotFoundError

        raise NotFoundError(detail="User not found")
    return await auth.get_refresh_token_pair(refresh_token, user)


@router.post("/force-logout", status_code=status.HTTP_204_NO_CONTENT)
async def force_logout(
    service: UserServiceDep,
    user: User = Depends(get_current_user),
) -> None:
    await service.force_logout(user.id)
