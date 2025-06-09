from typing import Any, Self
from fastapi import HTTPException, status


class UnauthorizedException(HTTPException):
    def __init__(
        self: Self,
        headers: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
            headers=headers,
        )


class InactiveUserException(HTTPException):
    def __init__(
        self: Self,
        headers: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User inactive.",
            headers=headers,
        )


class ExpiredToken(HTTPException):
    def __init__(
        self: Self,
        headers: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers=headers,
        )


class InvalidToken(HTTPException):
    def __init__(
        self: Self,
        headers: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers=headers,
        )


class InvalidTokenType(HTTPException):
    def __init__(
        self: Self,
        token_type: str,
        expected_type: str,
        headers: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Invalid token type '{token_type}', expected '{expected_type}'.",
            headers=headers,
        )


class NotEnoughPermissions(HTTPException):
    def __init__(
        self: Self,
        headers: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions.",
            headers=headers,
        )
