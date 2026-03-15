import enum


class Currency(str, enum.Enum):
    UAH = "UAH"
    USD = "USD"
    EUR = "EUR"


class SortOrder(str, enum.Enum):
    asc = "asc"
    desc = "desc"
