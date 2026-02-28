from typing import Annotated

from fastapi import Depends

from .compay_service import CompanyService
from .item_service import ItemService
from ..repo import get_repo_company, CompanyRepository, ItemRepository, get_repo_item


def get_company_service(repo: Annotated[CompanyRepository, Depends(get_repo_company)]) -> CompanyService:
    return CompanyService(repo)


def get_item_service(repo: Annotated[ItemRepository, Depends(get_repo_item)]) -> ItemService:
    return ItemService(repo)
