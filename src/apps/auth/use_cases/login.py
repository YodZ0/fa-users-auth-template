from typing import Protocol

from src.apps.users.services.users import UsersServiceProtocol
from ..services.jwt_service import JWTServiceProtocol
from ..services.security import SecurityServiceProtocol
from ..schemas.credentials import CredentialsSchema
from ..schemas.tokens import TokenInfo, TokenCreateSchema
from ..exceptions import UnauthorizedException, InactiveUserException


class LoginUseCaseProtocol(Protocol):
    async def __call__(self, login_user: CredentialsSchema) -> TokenInfo: ...


class LoginUseCaseImpl:
    def __init__(
        self,
        users_service: UsersServiceProtocol,
        security_service: SecurityServiceProtocol,
        jwt_service: JWTServiceProtocol,
    ) -> None:
        self.users_service = users_service
        self.security_service = security_service
        self.jwt_service = jwt_service

    async def __call__(self, login_user: CredentialsSchema) -> TokenInfo:
        # 1. Get user from DB by username (users_service)
        try:
            user = await self.users_service.get_user_by_username(login_user.username)
        except Exception:
            raise UnauthorizedException

        # 2. Validate password (security service)
        if not self.security_service.validate_password(
            password=login_user.password,
            hashed_password=user.hashed_password,
        ):
            raise UnauthorizedException

        # 3. Check user is active
        if not user.is_active:
            raise InactiveUserException

        # 4. Create access+refresh tokens (jwt_service)
        access_token = self.jwt_service.create_access_token(user)
        refresh_token = self.jwt_service.create_refresh_token(user)

        # 5. Save refresh token in DB (jwt_service)
        token_save = TokenCreateSchema(token=refresh_token, user_id=user.id)
        await self.jwt_service.save_refresh_token(token_save)

        return TokenInfo(
            access_token=access_token,
            refresh_token=refresh_token,
        )
