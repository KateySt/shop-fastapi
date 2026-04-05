from dataclasses import dataclass

from fastapi import Query


@dataclass
class CompanyFilters:
    visible: bool | None = Query(None)
    name: str | None = Query(None, max_length=100)

    def to_dict(self) -> dict:
        return {"visible": self.visible, "name": self.name}
