from fastapi import APIRouter

from .depends import ReferencesRepository
from .schemas import ReferenceData

router = APIRouter(
    prefix="/references",
    tags=["References"],
)


@router.get("")
async def get_references(
    repository: ReferencesRepository,
) -> ReferenceData:
    result = await repository.get_all()
    return result
