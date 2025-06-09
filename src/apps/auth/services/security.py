import bcrypt
from typing import Protocol


class SecurityServiceProtocol(Protocol):

    @staticmethod
    def encode_password(password: str) -> bytes: ...

    @staticmethod
    def validate_password(
        password: str,
        hashed_password: bytes,
    ) -> bool: ...


class SecurityServiceImpl:

    @staticmethod
    def encode_password(password: str) -> bytes:
        """
        Hash password from string.
        """
        salt = bcrypt.gensalt()
        pwd_bytes: bytes = password.encode()
        return bcrypt.hashpw(password=pwd_bytes, salt=salt)

    @staticmethod
    def validate_password(password: str, hashed_password: bytes) -> bool:
        """
        Compare hashed_password with password from input.
        """
        return bcrypt.checkpw(
            password=password.encode(),
            hashed_password=hashed_password,
        )
