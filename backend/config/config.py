from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    redis_host: str = Field("localhost", validation_alias="REDIS_HOST")
    redis_port: int = Field(6379, validation_alias="REDIS_PORT")
    redis_db: int = Field(0, validation_alias="REDIS_DB")

    celery_broker_url: str = Field(
        "redis://localhost:6379/0", validation_alias="CELERY_BROKER_URL"
    )
    celery_result_backend: str = Field(
        "redis://localhost:6379/0", validation_alias="CELERY_RESULT_BACKEND"
    )

    secret_key: str = Field("89U2NOjW-I", validation_alias="SECRET_KEY")
    jwt_secret: str = Field("9VHleSjX-C", validation_alias="JWT_SECRET")
    algorithm: str = Field("HS256", validation_alias="ALGORITHM")
    access_token_expire_minutes: int = Field(
        30, validation_alias="ACCESS_TOKEN_EXPIRE_MINUTES"
    )

    daily_link_limit: int = Field(100, validation_alias="DAILY_LINK_LIMIT")
    link_count_ttl: int = Field(86400, validation_alias="LINK_COUNT_TTL")
    cache_ttl: int = Field(3600, validation_alias="CACHE_TTL")

    generate_unique_code_length: int = Field(
        6, validation_alias="GENERATE_UNIQUE_CODE_LENGTH"
    )
    qr_box_size: int = Field(10, validation_alias="QR_BOX_SIZE")
    qr_border: int = Field(4, validation_alias="QR_BORDER")

    database_url: str = Field("sqlite:///./test.db", validation_alias="DATABASE_URL")

    postgres_user: str = Field(None, validation_alias="POSTGRES_USER")
    postgres_password: str = Field(None, validation_alias="POSTGRES_PASSWORD")
    postgres_db: str = Field(None, validation_alias="POSTGRES_DB")
    postgres_host: str = Field(None, validation_alias="POSTGRES_HOST")
    postgres_port: int = Field(None, validation_alias="POSTGRES_PORT")

    google_client_id: Optional[str] = Field(None, validation_alias="GOOGLE_CLIENT_ID")
    google_client_secret: Optional[str] = Field(None, validation_alias="GOOGLE_CLIENT_SECRET")

    yandex_client_id: Optional[str] = Field(None, validation_alias="YANDEX_CLIENT_ID")
    yandex_client_secret: Optional[str] = Field(None, validation_alias="YANDEX_CLIENT_SECRET")

    frontend_url: str = Field("http://localhost:5173", validation_alias="FRONTEND_URL")
    backend_url: str = Field("http://localhost:8000", validation_alias="BACKEND_URL")

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()
