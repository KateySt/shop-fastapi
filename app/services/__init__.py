from typing import Annotated

from fastapi import Depends

from .abstract import AbstractCompanyService, AbstractItemService
from .company_service import CompanyService
from .impl.company_service_impl import CompanyServiceImpl
from .impl.item_service_impl import ItemServiceImpl
from .item_service import ItemService
from ..mappers import CompanyMapper, CompanyPaginatedMapper, get_company_mapper, get_company_paginated_mapper, \
    ItemMapper, get_item_mapper, ItemPaginatedMapper, get_item_paginated_mapper
from ..repo import get_repo_company, CompanyRepository, ItemRepository, get_repo_item


def get_company_service(
        repo: Annotated[CompanyRepository, Depends(get_repo_company)],
        mapper: Annotated[CompanyMapper, Depends(get_company_mapper)],
        paginated_mapper: Annotated[CompanyPaginatedMapper, Depends(get_company_paginated_mapper)],
) -> AbstractCompanyService:
    return CompanyService(
        impl=CompanyServiceImpl(repo),
        mapper=mapper,
        paginated_mapper=paginated_mapper,
    )


def get_item_service(
        repo: Annotated[ItemRepository, Depends(get_repo_item)],
        mapper: Annotated[ItemMapper, Depends(get_item_mapper)],
        paginated_mapper: Annotated[ItemPaginatedMapper, Depends(get_item_paginated_mapper)],
) -> AbstractItemService:
    return ItemService(
        impl=ItemServiceImpl(repo),
        mapper=mapper,
        paginated_mapper=paginated_mapper,
    )


CompanyServiceDep = Annotated[AbstractCompanyService, Depends(get_company_service)]
ItemServiceDep = Annotated[AbstractItemService, Depends(get_item_service)]
