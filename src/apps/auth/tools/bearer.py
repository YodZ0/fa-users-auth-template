from typing import Annotated

from jwt import InvalidTokenError, ExpiredSignatureError

from fastapi import Depends
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
)

from .jwts import decode_jwt
from ..enums import TokenPayloadFieldsEnum as tf
from ..schemas.tokens import TokenPayload
from ..exceptions import InvalidToken, ExpiredToken, InvalidTokenType

http_bearer = HTTPBearer()


def get_current_token(
    credentials: Annotated[
        HTTPAuthorizationCredentials,
        Depends(http_bearer),
    ],
) -> str:
    """
    Fetch token from request Header (Authorization: Bearer <token>)
    """
    token: str = credentials.credentials
    return token


def get_current_token_payload(
    token: Annotated[str, Depends(get_current_token)],
) -> TokenPayload:
    """
    Decode and validate JWT
    :returns: TokenPayload(token: str, payload: dict)
    """
    try:
        payload = decode_jwt(token)
        token_payload = TokenPayload(token=token, payload=payload)
    except ExpiredSignatureError:
        raise ExpiredToken
    except InvalidTokenError:
        raise InvalidToken
    return token_payload


def get_valid_refresh_token(
    token: Annotated[
        TokenPayload,
        Depends(get_current_token_payload),
    ],
) -> TokenPayload:
    token_type = token.payload.get(tf.TOKEN_TYPE_FIELD)
    if token_type != tf.REFRESH_TOKEN_TYPE:
        raise InvalidTokenType(token_type, expected_type=tf.REFRESH_TOKEN_TYPE)
    return token


def get_valid_access_token(
    token: Annotated[
        TokenPayload,
        Depends(get_current_token_payload),
    ],
) -> TokenPayload:
    token_type = token.payload.get(tf.TOKEN_TYPE_FIELD)
    if token_type != tf.ACCESS_TOKEN_TYPE:
        raise InvalidTokenType(token_type, expected_type=tf.ACCESS_TOKEN_TYPE)
    return token


AccessToken = Annotated[TokenPayload, Depends(get_valid_access_token)]
RefreshToken = Annotated[TokenPayload, Depends(get_valid_refresh_token)]
