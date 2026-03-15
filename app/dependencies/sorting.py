from dataclasses import dataclass

from fastapi import Query

from app.db.models.enums import SortOrder


@dataclass
class SortingParams:
    order_by: str = Query("created_at")
    order: SortOrder = Query(SortOrder.desc)
