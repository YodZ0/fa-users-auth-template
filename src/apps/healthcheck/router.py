from fastapi import APIRouter
from src.core.schemas import SuccessResponseSchema

router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get("", response_model=SuccessResponseSchema)
async def health_check() -> SuccessResponseSchema:
    return SuccessResponseSchema()
