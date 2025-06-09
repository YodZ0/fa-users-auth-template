from typing import Protocol

from ..services.jwt_service import JWTServiceProtocol


class LogoutUseCaseProtocol(Protocol):
    async def __call__(self, token: str) -> bool: ...


class LogoutUseCaseImpl:
    def __init__(self, jwt_service: JWTServiceProtocol) -> None:
        self.jwt_service = jwt_service

    async def __call__(self, token: str) -> bool:
        await self.jwt_service.disable_refresh_token(token)
        return True
