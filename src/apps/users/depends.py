from typing import Annotated
from fastapi import Depends

from src.core.database import SessionDep

from .repositories.users import UsersRepositoryProtocol, UsersRepositoryImpl
from .services.users import UsersServiceProtocol, UsersServiceImpl
from .use_cases.user_info import UserInfoUseCaseProtocol, UserInfoUseCaseImpl


# === REPOSITORIES ===
def get_users_repository(session: SessionDep) -> UsersRepositoryProtocol:
    return UsersRepositoryImpl(session=session)


UsersRepository = Annotated[
    UsersRepositoryProtocol,
    Depends(get_users_repository),
]


# === SERVICES ===
def get_users_service(repository: UsersRepository) -> UsersServiceProtocol:
    return UsersServiceImpl(repository=repository)


UsersService = Annotated[
    UsersServiceProtocol,
    Depends(get_users_service),
]


# === USE CASES ===
def get_user_info_use_case(
    user_service: UsersService,
) -> UserInfoUseCaseProtocol:
    return UserInfoUseCaseImpl(users_service=user_service)


UserInfoUseCase = Annotated[
    UserInfoUseCaseProtocol,
    Depends(get_user_info_use_case),
]
