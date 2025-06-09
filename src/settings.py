from pathlib import Path

from pydantic import BaseModel
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent  # ../backend
CERTS_DIR = BASE_DIR / "certs"
CERTS_DIR.mkdir(parents=True, exist_ok=True)  # create "backend/certs" dir if not exist


class AdminConfig(BaseModel):
    admin_title: str = "Starlette Admin"
    secret_key: str
    session_cookie: str = "session"
    session_max_age: int = 60 * 60 * 24  # 1 day


class RunConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8000


class ApiPrefix(BaseModel):
    prefix: str = "/api"


class AuthJWTConfig(BaseModel):
    private_key_path: Path = CERTS_DIR / "jwt-private.pem"
    public_key_path: Path = CERTS_DIR / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7


class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    max_overflow: int = 10
    pool_size: int = 50


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        env_file=(BASE_DIR / ".env"),
        extra="ignore",
    )

    base_dir: Path = BASE_DIR
    cors_origins: list[str]
    admin: AdminConfig
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()
    auth_jwt: AuthJWTConfig = AuthJWTConfig()
    db: DatabaseConfig


settings = Settings()
