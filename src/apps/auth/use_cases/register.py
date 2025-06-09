from typing import Self, Protocol

from src.apps.users.services.users import UsersServiceProtocol
from src.apps.users.schemas.users import UserCreateSchema

from ..services.security import SecurityServiceProtocol
from ..schemas.credentials import CredentialsSchema
from ..exceptions import UnauthorizedException


class RegisterUseCaseProtocol(Protocol):

    async def __call__(self: Self, register_schema: CredentialsSchema) -> bool: ...


class RegisterUseCaseImpl:
    def __init__(
        self: Self,
        security_service: SecurityServiceProtocol,
        users_service: UsersServiceProtocol,
    ) -> None:
        self.security_service = security_service
        self.users_service = users_service

    async def __call__(self: Self, register_schema: CredentialsSchema) -> bool:
        # 1. Hash input password
        hashed_password = self.security_service.encode_password(
            password=register_schema.password,
        )
        # 2. Create new user
        new_user = UserCreateSchema(
            username=register_schema.username,
            hashed_password=hashed_password,
        )
        try:
            await self.users_service.register_user(new_user)
        except Exception:
            raise UnauthorizedException
        return True
