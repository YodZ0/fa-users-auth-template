from sqlalchemy import select, update

from src.core.repositories.db_repository import (
    DBRepositoryProtocol,
    DBRepositoryImpl,
)
from src.core.models.auth_token import AuthToken
from src.core.exceptions import ModelNotFoundException

from ..schemas.tokens import (
    TokenReadSchema,
    TokenCreateSchema,
    TokenUpdateSchema,
)


class AuthTokensRepositoryProtocol(
    DBRepositoryProtocol[
        AuthToken,
        TokenReadSchema,
        TokenCreateSchema,
        TokenUpdateSchema,
    ],
):
    async def set_token_used(self, token: str) -> bool: ...

    async def get_token(self, token: str) -> TokenReadSchema: ...


class AuthTokensRepositoryImpl(
    AuthTokensRepositoryProtocol,
    DBRepositoryImpl[
        AuthToken,
        TokenReadSchema,
        TokenCreateSchema,
        TokenUpdateSchema,
    ],
):
    model_type = AuthToken
    read_schema_type = TokenReadSchema

    async def set_token_used(self, token: str) -> bool:
        async with self.session as s, s.begin():
            statement = (
                update(self.model_type)
                .where(self.model_type.token == token)
                .values(is_used=True)
            )
            await s.execute(statement)
            return True

    async def get_token(self, token: str) -> TokenReadSchema:
        async with self.session as s:
            statement = select(self.model_type).where(self.model_type.token == token)
            model = (await s.execute(statement)).scalar_one_or_none()
            if model is None:
                raise ModelNotFoundException(self.model_type)
            return self.read_schema_type.model_validate(model, from_attributes=True)
