from enum import Enum, StrEnum


class Currency(str, Enum):
    UAH = "UAH"
    USD = "USD"
    EUR = "EUR"


class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"


class UserPermissionsEnum(StrEnum):
    CAN_SEE_USERS = "CAN_SEE_USERS"
    CAN_SELF_DELETE = "CAN_SELF_DELETE"


class MessageType(str, Enum):
    TEXT = "text"
    JOIN = "join"
    LEAVE = "leave"
    ERROR = "error"
    PING = "ping"
    PONG = "pong"
