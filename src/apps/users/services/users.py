import uuid
from typing import Protocol

from ..repositories.users import UsersRepositoryProtocol
from ..schemas.users import UserReadSchema, UserCreateSchema, UserResponseSchema


class UsersServiceProtocol(Protocol):
    async def register_user(self, new_user: UserCreateSchema) -> bool: ...

    async def get_user_by_username(self, username: str) -> UserReadSchema: ...

    async def get_user_by_uuid(self, user_id: uuid.UUID) -> UserResponseSchema: ...


class UsersServiceImpl:
    def __init__(self, repository: UsersRepositoryProtocol) -> None:
        self.repository = repository

    async def register_user(self, new_user: UserCreateSchema) -> bool:
        try:
            await self.repository.create_user(new_user)
        except Exception:
            raise
        return True

    async def get_user_by_username(self, username: str) -> UserReadSchema:
        try:
            user = await self.repository.get_user_by_username(username)
        except Exception:
            raise
        return user

    async def get_user_by_uuid(self, user_id: uuid.UUID) -> UserResponseSchema:
        try:
            user = await self.repository.get_user_by_uuid(user_id)
            user_response = UserResponseSchema(
                **user.model_dump(exclude={"hashed_password"})
            )
        except Exception:
            raise
        return user_response
