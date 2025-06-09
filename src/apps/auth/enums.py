from enum import StrEnum, auto


class TokenPayloadFieldsEnum(StrEnum):
    """
    Enum of all JWT fields.
    """

    SUB_FIELD = "sub"
    TOKEN_TYPE_FIELD = "type"
    ACCESS_TOKEN_TYPE = "access"
    REFRESH_TOKEN_TYPE = "refresh"
    ROLES_FIELD = "roles"


class ActionsEnum(StrEnum):
    CREATE = auto()
    VIEW = auto()
    EDIT = auto()
    DELETE = auto()


class ResourcesEnum(StrEnum):
    PATIENTS = auto()
    USERS = auto()
    LAB = auto()
    REPORTS = auto()
