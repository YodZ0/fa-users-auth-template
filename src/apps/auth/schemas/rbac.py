from pydantic import BaseModel
from src.core.schemas import CreateBaseModel, UpdateBaseModel
from ..enums import ResourcesEnum, ActionsEnum


class PermissionReadSchema(BaseModel):
    pass


class PermissionCreateSchema(CreateBaseModel):
    pass


class PermissionUpdateSchema(UpdateBaseModel):
    pass


class RolePermissions(BaseModel):
    role: str
    permissions: dict[ResourcesEnum, list[ActionsEnum]]


class AccessControlMap(BaseModel):
    roles: dict[str, dict[ResourcesEnum, list[ActionsEnum]]]
