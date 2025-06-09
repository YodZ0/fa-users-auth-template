import uuid

from sqlalchemy import select, insert
from sqlalchemy.orm import selectinload

from src.core.repositories.db_repository import (
    DBRepositoryProtocol,
    DBRepositoryImpl,
)
from src.core.models.users import User
from src.core.exceptions import ModelNotFoundException

from ..schemas.users import (
    UserReadSchema,
    UserCreateSchema,
    UserUpdateSchema,
)


class UsersRepositoryProtocol(
    DBRepositoryProtocol[
        User,
        UserReadSchema,
        UserCreateSchema,
        UserUpdateSchema,
    ],
):
    async def create_user(self, create_object: UserCreateSchema) -> uuid.UUID: ...

    async def get_user_by_username(self, username: str) -> UserReadSchema: ...

    async def get_user_by_uuid(self, uid: uuid.UUID) -> UserReadSchema: ...


class UsersRepositoryImpl(
    UsersRepositoryProtocol,
    DBRepositoryImpl[
        User,
        UserReadSchema,
        UserCreateSchema,
        UserUpdateSchema,
    ],
):
    model_type = User
    read_schema_type = UserReadSchema

    async def create_user(self, create_object: UserCreateSchema) -> uuid.UUID:
        async with self.session as s, s.begin():
            statement = (
                insert(self.model_type)
                .values(**create_object.model_dump(exclude={"id"}))
                .returning(self.model_type.id)
            )
            model = (await s.execute(statement)).scalar_one()
            return model

    async def get_user_by_username(self, username: str) -> UserReadSchema:
        async with self.session as s:
            statement = (
                select(self.model_type)
                .filter_by(username=username)
                .options(selectinload(self.model_type.roles))
            )
            model = (await s.execute(statement)).scalar_one_or_none()
            if model is None:
                raise ModelNotFoundException(self.model_type)

            model_dict = model.__dict__.copy()
            model_dict["roles"] = [role.name for role in model.roles]

            return self.read_schema_type.model_validate(
                model_dict,
                from_attributes=True,
            )

    async def get_user_by_uuid(self, uid: uuid.UUID) -> UserReadSchema:
        async with self.session as s:
            statement = (
                select(self.model_type)
                .filter_by(id=uid)
                .options(selectinload(self.model_type.roles))
            )
            model = (await s.execute(statement)).scalar_one_or_none()
            if model is None:
                raise ModelNotFoundException(self.model_type)

            model_dict = model.__dict__.copy()
            model_dict["roles"] = [role.name for role in model.roles]

            return self.read_schema_type.model_validate(
                model_dict,
                from_attributes=True,
            )
