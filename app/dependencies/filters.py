from dataclasses import dataclass

from fastapi import Query


@dataclass
class CompanyFilters:
    visible: bool | None = Query(None)
    name: str | None = Query(None, max_length=100)
