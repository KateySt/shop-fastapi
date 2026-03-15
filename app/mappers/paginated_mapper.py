from collections.abc import Sequence
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, TypeAdapter

ORM_T = TypeVar("ORM_T")
RESPONSE_T = TypeVar("RESPONSE_T", bound=BaseModel)


class PaginatedMapper(Generic[ORM_T, RESPONSE_T]):

    def __init__(
        self,
        orm_class: type[ORM_T],
        response_class: type[RESPONSE_T],
        item_schema: type[BaseModel],
    ):
        self.orm_class = orm_class
        self.response_class = response_class
        self._adapter: TypeAdapter[Any] = TypeAdapter(list[item_schema])  # type: ignore[valid-type]

    def from_orm_list(
        self,
        orm_list: Sequence[ORM_T],
        total: int,
        skip: int = 0,
        limit: int = 20,
    ) -> RESPONSE_T:
        items = self._adapter.validate_python(orm_list, from_attributes=True)
        return self.response_class(
            items=items,
            total=total,
            skip=skip,
            limit=limit,
        )
