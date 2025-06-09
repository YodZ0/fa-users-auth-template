import uuid
from typing import Optional, List, Dict, Any, Generic, TypeVar, Literal
from pydantic import AliasGenerator, BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class SuccessResponseSchema(BaseModel):
    status: str = "OK"


class RequestSchema(BaseModel):
    """
    Request API schema.
    """

    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            validation_alias=to_camel,
        )
    )


class ResponseSchema(BaseModel):
    """
    Response API schema.
    """

    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            serialization_alias=to_camel,
        )
    )


class CreateBaseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class UpdateBaseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID | int


class FilterBaseModel(BaseModel):
    model_config = ConfigDict(extra="ignore")


SortOrder = Literal["asc", "desc"]


class SortSchema(BaseModel):
    field: str
    order: SortOrder = "desc"


class QuerySchema(BaseModel):
    limit: int = Field(default=10, gt=0, le=50)
    offset: int = Field(default=0, ge=0)
    sort: Optional[List[SortSchema]] = None
    filters: Optional[Dict[str, Any]] = None


TRead = TypeVar("TRead")


class PaginationResultSchema(BaseModel, Generic[TRead]):
    objects: list[TRead]
    count: int
