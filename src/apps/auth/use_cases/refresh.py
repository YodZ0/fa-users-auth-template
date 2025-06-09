from typing import Protocol

from src.apps.users.services.users import UsersServiceProtocol
from ..services.jwt_service import JWTServiceProtocol
from ..schemas.tokens import TokenPayload, TokenInfo
from ..enums import TokenPayloadFieldsEnum as tf
from ..exceptions import InactiveUserException, InvalidToken


class RefreshUseCaseProtocol(Protocol):

    async def __call__(self, token: TokenPayload) -> TokenInfo: ...


class RefreshUseCaseImpl:
    def __init__(
        self,
        users_service: UsersServiceProtocol,
        jwt_service: JWTServiceProtocol,
    ) -> None:
        self.users_service = users_service
        self.jwt_service = jwt_service

    async def __call__(self, token: TokenPayload) -> TokenInfo:
        # 1. Get token from DB
        try:
            token_db = await self.jwt_service.get_refresh_token(token=token.token)
        except Exception:
            raise InvalidToken
        if token_db.is_used:
            raise InvalidToken
        # 2. Get user from DB
        payload = token.payload
        sub = payload.get(tf.SUB_FIELD)
        user = await self.users_service.get_user_by_uuid(user_id=sub)
        # 3. If user active
        if not user.is_active:
            raise InactiveUserException
        # 4. Create access token
        access_token = self.jwt_service.create_access_token(user_schema=user)
        return TokenInfo(access_token=access_token)
