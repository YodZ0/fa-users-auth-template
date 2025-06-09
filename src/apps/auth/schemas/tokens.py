import uuid
from pydantic import BaseModel
from src.core.schemas import CreateBaseModel, UpdateBaseModel, ResponseSchema


class TokenPayload(BaseModel):
    token: str | None = None
    payload: dict


class TokenInfo(ResponseSchema):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"


class TokenReadSchema(BaseModel):
    id: int
    token: str
    user_id: uuid.UUID
    is_used: bool


class TokenCreateSchema(CreateBaseModel):
    token: str
    user_id: uuid.UUID
    is_used: bool = False


class TokenUpdateSchema(UpdateBaseModel):
    id: int | None = None
    token: str
    is_used: bool = True
