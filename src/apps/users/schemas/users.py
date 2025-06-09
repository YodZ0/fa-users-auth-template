import uuid
from typing import Optional
from pydantic import ConfigDict

from src.core.schemas import CreateBaseModel, UpdateBaseModel, ResponseSchema


class UserResponseSchema(ResponseSchema):
    model_config = ConfigDict(extra="ignore")

    id: uuid.UUID
    username: str
    is_active: bool
    roles: list[str]


class UserReadSchema(ResponseSchema):
    model_config = ConfigDict(extra="ignore")

    id: uuid.UUID
    username: str
    hashed_password: bytes
    is_active: bool
    roles: list[str]


class UserCreateSchema(CreateBaseModel):
    username: str
    hashed_password: bytes
    is_active: bool = True


class UserUpdateSchema(UpdateBaseModel):
    id: uuid.UUID
    old_password: str
    new_password: str
