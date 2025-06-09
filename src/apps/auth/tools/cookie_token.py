from typing import Annotated, Optional

from fastapi import Depends, Request

from jwt import InvalidTokenError, ExpiredSignatureError

from .jwts import decode_jwt
from ..schemas.tokens import TokenPayload
from ..exceptions import UnauthorizedException, InvalidToken, ExpiredToken


def get_refresh_token_from_cookie(request: Request) -> Optional[str]:
    refresh_token = request.cookies.get("refreshToken")
    if refresh_token:
        return refresh_token
    raise UnauthorizedException


def get_refresh_token(
    token: Annotated[
        str,
        Depends(get_refresh_token_from_cookie),
    ],
) -> TokenPayload:
    try:
        payload = decode_jwt(token)
        token_payload = TokenPayload(token=token, payload=payload)
    except ExpiredSignatureError:
        raise ExpiredToken
    except InvalidTokenError:
        raise InvalidToken
    return token_payload


CookieRefreshToken = Annotated[TokenPayload, Depends(get_refresh_token)]
