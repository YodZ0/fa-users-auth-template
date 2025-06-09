import uuid
from pydantic import BaseModel
from typing import Protocol, TypeVar, Any, List, Dict

from sqlalchemy import select, insert, update, delete
from sqlalchemy.sql import Select
from sqlalchemy.sql.elements import UnaryExpression
from sqlalchemy.sql.expression import func
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.base import Base
from ..schemas import (
    CreateBaseModel,
    UpdateBaseModel,
    PaginationResultSchema,
    SortSchema,
)
from ..exceptions import (
    ModelNotFoundException,
    SortingFieldNotFoundError,
)


ModelType = TypeVar("ModelType", bound=Base, covariant=True)
ReadSchemaType = TypeVar("ReadSchemaType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=CreateBaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=UpdateBaseModel)


class DBRepositoryProtocol(
    Protocol[
        ModelType,
        ReadSchemaType,
        CreateSchemaType,
        UpdateSchemaType,
    ]
):
    async def get_one(self, id_: uuid.UUID | int) -> ReadSchemaType: ...

    async def get_all(self) -> List[ReadSchemaType]: ...

    async def create(self, create_object: CreateSchemaType) -> ReadSchemaType: ...

    async def update(self, update_object: UpdateSchemaType) -> ReadSchemaType: ...

    async def delete(self, id_: uuid.UUID | int) -> bool: ...

    async def filter(self, filters: Dict[str, Any] = None) -> ReadSchemaType: ...

    async def query_all(
        self,
        limit: int,
        offset: int,
        filters: Dict[str, Any] = None,
        sorting: List[SortSchema] = None,
    ) -> PaginationResultSchema[ReadSchemaType]: ...

    async def _filter(self, statement: Select, filters: Dict[str, Any]) -> Select: ...

    async def _paginate(self, statement: Select, limit: int, offset: int) -> Select: ...

    async def _sort(self, statement: Select, sorting: List[SortSchema]) -> Select: ...


class DBRepositoryImpl(
    DBRepositoryProtocol[
        ModelType,
        ReadSchemaType,
        CreateSchemaType,
        UpdateSchemaType,
    ]
):
    model_type: type[ModelType]
    read_schema_type: type[ReadSchemaType]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_one(self, id_: uuid.UUID | int) -> ReadSchemaType:
        async with self.session as s:
            statement = select(self.model_type).where(self.model_type.id == id_)
            model = (await s.execute(statement)).scalar_one_or_none()
            if model is None:
                raise ModelNotFoundException(self.model_type, id_)
            return self.read_schema_type.model_validate(model, from_attributes=True)

    async def get_all(self) -> List[ReadSchemaType]:
        async with self.session as s:
            statement = select(self.model_type)
            models = (await s.execute(statement)).scalars().all()
            return [
                self.read_schema_type.model_validate(model, from_attributes=True)
                for model in models
            ]

    async def create(self, create_object: CreateSchemaType) -> ReadSchemaType:
        async with self.session as s, s.begin():
            statement = (
                insert(self.model_type)
                .values(**create_object.model_dump(exclude={"id"}))
                .returning(self.model_type)
            )
            model = (await s.execute(statement)).scalar_one()
            return self.read_schema_type.model_validate(model, from_attributes=True)

    async def update(self, update_object: UpdateSchemaType) -> ReadSchemaType:
        async with self.session as s, s.begin():
            pk = update_object.id
            statement = (
                update(self.model_type)
                .where(self.model_type.id == pk)
                .values(update_object.model_dump(exclude={"id"}, exclude_unset=True))
                .returning(self.model_type)
            )
            model = (await s.execute(statement)).scalar_one_or_none()
            if model is None:
                raise ModelNotFoundException(self.model_type, update_object.id)
            return self.read_schema_type.model_validate(model, from_attributes=True)

    async def delete(self, id_: uuid.UUID | int) -> bool:
        async with self.session as s, s.begin():
            statement = delete(self.model_type).where(self.model_type.id == id_)
            await s.execute(statement)
            return True

    async def filter(self, filters: Dict[str, Any] = None) -> ReadSchemaType:
        async with self.session as s:
            statement = select(self.model_type)
            statement = await self._filter(statement, filters)
            model = (await s.execute(statement)).scalar_one_or_none()
            if model is None:
                raise ModelNotFoundException(self.model_type)
            return self.read_schema_type.model_validate(model, from_attributes=True)

    async def query_all(
        self,
        limit: int,
        offset: int,
        filters: Dict[str, Any] = None,
        sorting: List[SortSchema] = None,
    ) -> PaginationResultSchema[ReadSchemaType]:
        async with self.session as s:
            statement = select(self.model_type)

            statement = await self._filter(statement, filters)

            count_statement = select(func.count()).select_from(statement.subquery())
            count = (await s.execute(count_statement)).scalar_one()

            statement = await self._sort(statement, sorting)
            statement = await self._paginate(statement, limit, offset)

            models = (await s.execute(statement)).scalars().all()
            objects = [
                self.read_schema_type.model_validate(model, from_attributes=True)
                for model in models
            ]

            return PaginationResultSchema(count=count, objects=objects)

    async def _filter(self, statement: Select, filters: Dict[str, Any]) -> Select:
        if filters:
            for field, value in filters.items():
                column = getattr(self.model_type, field, None)
                if column is not None:
                    if isinstance(value, list):
                        statement = statement.where(column.in_(value))
                    else:
                        statement = statement.where(column == value)
        return statement

    async def _paginate(self, statement: Select, limit: int, offset: int) -> Select:
        return statement.limit(limit).offset(offset)

    async def _sort(self, statement: Select, sorting: List[SortSchema]) -> Select:
        if sorting:
            order_by_expr = self.get_order_by_expr(sorting)
            statement = statement.order_by(*order_by_expr)
        return statement

    def get_order_by_expr(self, sorting: List[SortSchema]) -> List[UnaryExpression]:
        order_by_expr: List[UnaryExpression] = []
        for st in sorting:
            try:
                if st.order == "desc":
                    order_by_expr.append(getattr(self.model_type, st.field).desc())
                else:
                    order_by_expr.append(getattr(self.model_type, st.field))
            except AttributeError as attribute_error:
                raise SortingFieldNotFoundError(st.field) from attribute_error
        return order_by_expr
