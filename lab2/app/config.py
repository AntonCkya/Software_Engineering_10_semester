from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AuthSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="AUTH_", env_file=".env", extra="ignore"
    )

    # Настройки для аутентификации
    jwt_secret_key: str = Field(default="your-super-duper-secret-key-aoaoaoa")
    jwt_algorithm: str = Field(default="HS256")
    access_token_expire_minutes: int = Field(default=30)
    refresh_token_expire_days: int = Field(default=7)


class ServerSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="SERVER_", env_file=".env", extra="ignore"
    )

    # Параметры запуска сервера
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8000)
    debug: bool = Field(default=False)
    reload: bool = Field(default=False)
    workers: int = Field(default=1)


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="APP_", env_file=".env", extra="ignore"
    )

    # Параметры для документации сервера
    name: str = Field(default="MeowMeowExpress")
    version: str = Field(default="0.0.1")
    description: str = Field(default="Сервис доставки ваших посылок <3")
    docs_url: str = Field(default="/docs", description="Путь до сваггера")
    redoc_url: str = Field(default="/redoc", description="Путь до redoc")
    openapi_url: str = Field(
        default="/openapi.json", description="Путь до чистой openapi спеки"
    )

    # Параметры для CORS (без них фронтенды не работают)
    cors_allow_origins_raw: str = Field(default="*", alias="CORS_ALLOW_ORIGINS")
    cors_allow_credentials_raw: bool = Field(
        default=True, alias="CORS_ALLOW_CREDENTIALS"
    )
    cors_allow_methods_raw: str = Field(default="*", alias="CORS_ALLOW_METHODS")
    cors_allow_headers_raw: str = Field(default="*", alias="CORS_ALLOW_HEADERS")

    @property
    def cors_allow_origins(self) -> list[str]:
        if self.cors_allow_origins_raw == "*":
            return ["*"]
        return [origin.strip() for origin in self.cors_allow_origins_raw.split(",")]

    @property
    def cors_allow_credentials(self) -> bool:
        return self.cors_allow_credentials_raw

    @property
    def cors_allow_methods(self) -> list[str]:
        if self.cors_allow_methods_raw == "*":
            return ["*"]
        return [method.strip() for method in self.cors_allow_methods_raw.split(",")]

    @property
    def cors_allow_headers(self) -> list[str]:
        if self.cors_allow_headers_raw == "*":
            return ["*"]
        return [header.strip() for header in self.cors_allow_headers_raw.split(",")]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    environment: str = Field(default="dev")

    auth: AuthSettings = Field(default_factory=AuthSettings)
    server: ServerSettings = Field(default_factory=ServerSettings)
    app: AppSettings = Field(default_factory=AppSettings)


@lru_cache  # чтобы 1 раз создалось
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
