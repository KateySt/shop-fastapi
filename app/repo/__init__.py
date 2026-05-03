from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.database import get_db_session
from .company_repository import CompanyRepository
from .item_repository import ItemRepository
from .message_repo import MessageRepository
from .order_repository import OrderRepository
from .user_repository import UserRepository


def get_repo_company(
    session: Annotated[AsyncSession, Depends(get_db_session)]
) -> CompanyRepository:
    return CompanyRepository(session)


def get_repo_item(
    session: Annotated[AsyncSession, Depends(get_db_session)]
) -> ItemRepository:
    return ItemRepository(session)


def get_repo_user(
    session: Annotated[AsyncSession, Depends(get_db_session)]
) -> UserRepository:
    return UserRepository(session)


def get_repo_order(
    session: Annotated[AsyncSession, Depends(get_db_session)]
) -> OrderRepository:
    return OrderRepository(session)


def get_repo_message(
    session: Annotated[AsyncSession, Depends(get_db_session)]
) -> MessageRepository:
    return MessageRepository(session)
