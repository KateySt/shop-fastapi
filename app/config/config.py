from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseSettings):
    APP_NAME: str = "shop"
    APP_ENV: str = "development"
    DEBUG: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="allow",
    )


class DBConfig(BaseSettings):
    DATABASE_URL: str
    DB_ECHO: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="allow",
    )


class SentryConfig(BaseSettings):
    SENTRY_DNS: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="allow",
    )


class LogConfig(BaseSettings):
    BETTER_STACK_TOKEN: str
    BETTER_STACK_URL: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="allow",
    )


class AuthConfig(BaseSettings):
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_TIME_MINUTES: int = 30
    REFRESH_TOKEN_TIME_MINUTES: int = 10080

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="allow",
    )


class RedisConfig(BaseSettings):
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_USER: str
    REDIS_PASSWORD: str
    REDIS_DATABASE: int = 0

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="allow",
    )


class S3Config(BaseSettings):
    S3_ENDPOINT: str
    S3_ACCESS_KEY: str
    S3_SECRET_KEY: str
    S3_PUBLIC_URL: str
    S3_REGION: str
    S3_BUCKET: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="allow",
    )


class StripeConfig(BaseSettings):
    STRIPE_SECRET_KEY: str
    STRIPE_PUBLISHABLE_KEY: str
    STRIPE_WEBHOOK_SECRET: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="allow",
    )


stripe_config = StripeConfig()
s3_config = S3Config()
app_config = AppConfig()
db_config = DBConfig()
log_config = LogConfig()
sentry_config = SentryConfig()
auth_config = AuthConfig()
redis_config = RedisConfig()
