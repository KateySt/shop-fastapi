from typing import Annotated

from fastapi import Depends

from app.dependencies.filters import CompanyFilters
from app.dependencies.pagination import PaginationParams
from app.dependencies.sorting import SortingParams

Pagination = Annotated[PaginationParams, Depends(PaginationParams)]
CompanyFiltersDep = Annotated[CompanyFilters, Depends(CompanyFilters)]
Sorting = Annotated[SortingParams, Depends(SortingParams)]
