from typing import Annotated
from fastapi import Depends

from src.core.database.db_provider import SessionDep
from .repository import ReferencesRepositoryProtocol, ReferencesRepositoryImpl


def get_references_repository(session: SessionDep) -> ReferencesRepositoryProtocol:
    return ReferencesRepositoryImpl(session=session)


ReferencesRepository = Annotated[
    ReferencesRepositoryProtocol,
    Depends(get_references_repository),
]
