from collections.abc import Sequence
from typing import Any, Generic, TypeVar

from pydantic import BaseModel

ORM_T = TypeVar("ORM_T")
CREATE_T = TypeVar("CREATE_T", bound=BaseModel)
UPDATE_T = TypeVar("UPDATE_T", bound=BaseModel)
RESPONSE_T = TypeVar("RESPONSE_T", bound=BaseModel)
INTERNAL_T = TypeVar("INTERNAL_T", bound=BaseModel)


class BaseMapper(Generic[ORM_T, CREATE_T, UPDATE_T, RESPONSE_T]):
    def __init__(
        self,
        orm_class: type[ORM_T],
        response_class: type[RESPONSE_T],
    ):
        self.orm_class = orm_class
        self.response_class = response_class

    def to_response(self, orm: ORM_T) -> RESPONSE_T:
        return self.response_class.model_validate(orm)

    def to_response_list(self, orm_list: Sequence[ORM_T]) -> list[RESPONSE_T]:
        return [self.to_response(item) for item in orm_list]

    def from_create(self, dto: CREATE_T, **extra: Any) -> ORM_T:
        data = dto.model_dump()
        data.update(extra)
        return self.orm_class(**data)

    def from_update(self, dto: UPDATE_T) -> dict:
        return dto.model_dump(exclude_unset=True)

    def to_paginated(
        self,
        orm_list: Sequence[ORM_T],
        total: int,
        skip: int,
        limit: int,
    ) -> dict:
        return {
            "items": self.to_response_list(orm_list),
            "total": total,
            "skip": skip,
            "limit": limit,
        }
