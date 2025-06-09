from typing import Annotated
from fastapi import Depends

from src.core.database import SessionDep
from src.apps.users.depends import UsersService

from .repositories.auth_tokens import (
    AuthTokensRepositoryProtocol,
    AuthTokensRepositoryImpl,
)
from .repositories.permissions import (
    PermissionsRepositoryProtocol,
    PermissionsRepositoryImpl,
)

from .services.jwt_service import JWTServiceProtocol, JWTServiceImpl
from .services.security import SecurityServiceProtocol, SecurityServiceImpl

from .use_cases.register import RegisterUseCaseProtocol, RegisterUseCaseImpl
from .use_cases.login import LoginUseCaseProtocol, LoginUseCaseImpl
from .use_cases.logout import LogoutUseCaseProtocol, LogoutUseCaseImpl
from .use_cases.refresh import RefreshUseCaseProtocol, RefreshUseCaseImpl


# === REPOSITORIES ===
def get_jwt_repository(session: SessionDep) -> AuthTokensRepositoryProtocol:
    return AuthTokensRepositoryImpl(session=session)


JWTRepository = Annotated[
    AuthTokensRepositoryProtocol,
    Depends(get_jwt_repository),
]


def get_perms_repository(session: SessionDep) -> PermissionsRepositoryProtocol:
    return PermissionsRepositoryImpl(session=session)


PermissionsRepository = Annotated[
    PermissionsRepositoryProtocol,
    Depends(get_perms_repository),
]


# === SERVICES ===
def get_security_service() -> SecurityServiceProtocol:
    return SecurityServiceImpl()


def get_jwt_service(repository: JWTRepository) -> JWTServiceProtocol:
    return JWTServiceImpl(repository=repository)


SecurityService = Annotated[
    SecurityServiceProtocol,
    Depends(get_security_service),
]
JWTService = Annotated[
    JWTServiceProtocol,
    Depends(get_jwt_service),
]


# === USE CASES ===
def get_register_use_case(
    users_service: UsersService,
    security_service: SecurityService,
) -> RegisterUseCaseProtocol:
    return RegisterUseCaseImpl(
        users_service=users_service,
        security_service=security_service,
    )

def get_login_use_case(
    users_service: UsersService,
    security_service: SecurityService,
    jwt_service: JWTService,
) -> LoginUseCaseProtocol:
    return LoginUseCaseImpl(
        users_service=users_service,
        security_service=security_service,
        jwt_service=jwt_service,
    )


def get_logout_use_case(jwt_service: JWTService) -> LogoutUseCaseProtocol:
    return LogoutUseCaseImpl(jwt_service=jwt_service)


def get_refresh_use_case(
    users_service: UsersService,
    jwt_service: JWTService,
) -> RefreshUseCaseProtocol:
    return RefreshUseCaseImpl(
        users_service=users_service,
        jwt_service=jwt_service,
    )

RegisterUseCase = Annotated[
    RegisterUseCaseProtocol,
    Depends(get_register_use_case),
]
LoginUseCase = Annotated[
    LoginUseCaseProtocol,
    Depends(get_login_use_case),
]
LogoutUseCase = Annotated[
    LogoutUseCaseProtocol,
    Depends(get_logout_use_case),
]
RefreshUseCase = Annotated[
    RefreshUseCaseProtocol,
    Depends(get_refresh_use_case),
]
