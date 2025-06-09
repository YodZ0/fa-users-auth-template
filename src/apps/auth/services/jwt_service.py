from datetime import timedelta
from typing import Protocol

from src.settings import settings
from src.apps.users.schemas.users import UserReadSchema

from ..repositories.auth_tokens import AuthTokensRepositoryProtocol
from ..schemas.tokens import TokenCreateSchema, TokenReadSchema

from ..enums import TokenPayloadFieldsEnum as tf
from ..tools.jwts import encode_jwt


class JWTServiceProtocol(Protocol):

    def create_access_token(self, user_schema: UserReadSchema) -> str: ...

    def create_refresh_token(self, user_schema: UserReadSchema) -> str: ...

    async def get_refresh_token(self, token: str) -> TokenReadSchema: ...

    async def save_refresh_token(self, token: TokenCreateSchema) -> None: ...

    async def disable_refresh_token(self, token: str) -> None: ...

    @staticmethod
    def _create_jwt(
        token_type: str,
        token_data: dict,
        expire_time_minutes: int,
        expire_timedelta: timedelta | None,
    ) -> str: ...


class JWTServiceImpl:
    def __init__(
        self,
        token_type: str = tf.ACCESS_TOKEN_TYPE,
        repository: AuthTokensRepositoryProtocol | None = None,
    ) -> None:
        self.token_type = token_type
        self.repository = repository

    def create_access_token(self, user_schema: UserReadSchema) -> str:
        jwt_payload = {
            tf.SUB_FIELD: str(user_schema.id),
            tf.ROLES_FIELD: user_schema.roles,
        }
        return self._create_jwt(
            token_type=tf.ACCESS_TOKEN_TYPE,
            token_data=jwt_payload,
            expire_time_minutes=settings.auth_jwt.access_token_expire_minutes,
        )

    def create_refresh_token(self, user_schema: UserReadSchema) -> str:
        jwt_payload = {
            tf.SUB_FIELD: str(user_schema.id),
        }
        return self._create_jwt(
            token_type=tf.REFRESH_TOKEN_TYPE,
            token_data=jwt_payload,
            expire_timedelta=timedelta(
                days=settings.auth_jwt.refresh_token_expire_days
            ),
        )

    async def get_refresh_token(self, token: str) -> TokenReadSchema:
        return await self.repository.get_token(token=token)

    async def save_refresh_token(self, token: TokenCreateSchema) -> None:
        await self.repository.create(token)
        return None

    async def disable_refresh_token(self, token: str) -> None:
        await self.repository.set_token_used(token)
        return None

    @staticmethod
    def _create_jwt(
        token_type: str,
        token_data: dict,
        expire_time_minutes: int = settings.auth_jwt.access_token_expire_minutes,
        expire_timedelta: timedelta | None = None,
    ) -> str:
        jwt_payload = {tf.TOKEN_TYPE_FIELD: token_type}
        jwt_payload.update(token_data)
        return encode_jwt(
            payload=jwt_payload,
            expire_minutes=expire_time_minutes,
            expire_timedelta=expire_timedelta,
        )
