from fastapi import APIRouter
from src.apps.auth.tools.deps import CurrentUser
from .schemas.users import UserResponseSchema
from .depends import UserInfoUseCase


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("/profile", name="users.view")
async def get_user_info(
    use_case: UserInfoUseCase,
    user_id: CurrentUser,
) -> UserResponseSchema:
    return await use_case(user_id)
