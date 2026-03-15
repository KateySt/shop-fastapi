from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.database import get_db_session
from .company_repository import CompanyRepository
from .item_repository import ItemRepository


def get_repo_company(
    session: Annotated[AsyncSession, Depends(get_db_session)]
) -> CompanyRepository:
    return CompanyRepository(session)


def get_repo_item(
    session: Annotated[AsyncSession, Depends(get_db_session)]
) -> ItemRepository:
    return ItemRepository(session)
