from fastapi import APIRouter, Response

from src.core.schemas import SuccessResponseSchema
from .schemas.credentials import CredentialsSchema
from .schemas.tokens import TokenInfo

from .tools.cookie_token import CookieRefreshToken
from .depends import RegisterUseCase, LoginUseCase, LogoutUseCase, RefreshUseCase

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)

@router.post("/register")
async def register(
    use_case: RegisterUseCase,
    register_schema: CredentialsSchema,
):
    await use_case(register_schema)
    return {"ok": True}


@router.post("/login", response_model_exclude_none=True)
async def login(
    use_case: LoginUseCase,
    login_schema: CredentialsSchema,
    response: Response,
) -> TokenInfo:
    token_info = await use_case(login_schema)
    response.set_cookie(
        key="refreshToken",
        value=token_info.refresh_token,
        httponly=True,
    )
    return TokenInfo(access_token=token_info.access_token)


@router.post("/logout")
async def logout(
    use_case: LogoutUseCase,
    token: CookieRefreshToken,
    response: Response,
) -> SuccessResponseSchema:
    await use_case(token=token.token)
    response.delete_cookie(key="refreshToken", httponly=True)
    return SuccessResponseSchema()


@router.post("/refresh", response_model_exclude_none=True)
async def get_new_access_token(
    use_case: RefreshUseCase,
    token: CookieRefreshToken,
) -> TokenInfo:
    return await use_case(token=token)
