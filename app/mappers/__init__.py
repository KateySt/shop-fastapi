from functools import lru_cache

from .base_mapper import BaseMapper
from .company_mapper import CompanyMapper, CompanyPaginatedMapper
from .item_mapper import ItemPaginatedMapper, ItemMapper
from .paginated_mapper import PaginatedMapper


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
