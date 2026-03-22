from functools import lru_cache

from .base_mapper import BaseMapper
from .company_mapper import CompanyMapper, CompanyPaginatedMapper
from .item_mapper import ItemMapper, ItemPaginatedMapper
from .paginated_mapper import PaginatedMapper
from .user_mapper import UserMapper


@lru_cache
def get_company_mapper() -> CompanyMapper:
    return CompanyMapper()


@lru_cache
def get_company_paginated_mapper() -> CompanyPaginatedMapper:
    return CompanyPaginatedMapper()


@lru_cache
def get_item_mapper() -> ItemMapper:
    return ItemMapper()


@lru_cache
def get_item_paginated_mapper() -> ItemPaginatedMapper:
    return ItemPaginatedMapper()


@lru_cache
def get_user_mapper() -> UserMapper:
    return UserMapper()
