import uuid
from typing import Protocol

from ..services.users import UsersServiceProtocol
from ..schemas.users import UserResponseSchema


class UserInfoUseCaseProtocol(Protocol):
    async def __call__(self, user_id: uuid.UUID) -> UserResponseSchema: ...


class UserInfoUseCaseImpl:
    def __init__(self, users_service: UsersServiceProtocol) -> None:
        self.users_service = users_service

    async def __call__(self, user_id: uuid.UUID) -> UserResponseSchema:
        return await self.users_service.get_user_by_uuid(user_id)
