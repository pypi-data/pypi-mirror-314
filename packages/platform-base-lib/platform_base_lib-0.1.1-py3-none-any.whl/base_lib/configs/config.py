from pathlib import Path
from enum import Enum

from pydantic_settings import BaseSettings
from starlette.config import Config

import os


current_file_dir = os.path.dirname(os.path.realpath(__file__))
env_path_root = os.path.join(current_file_dir, "..", "..", ".env")


# Define the first path to check
relative_env_path = Path(__file__).resolve().parent.parent.parent / ".env"

# Define the fallback root folder path
fallback_env_path = (
    Path(__file__).resolve().parent.parent.parent.parent.parent.parent.parent / ".env"
)

# Check which file exists
if os.path.exists(env_path_root):
    env_path = env_path_root
elif relative_env_path.exists():
    env_path = relative_env_path
elif fallback_env_path.exists():
    env_path = fallback_env_path
else:
    raise FileNotFoundError("Could not find the .env file in the expected locations.")

config = Config(env_path)


class CryptSettings(BaseSettings):
    SECRET_KEY: str = config("SECRET_KEY")
    ALGORITHM: str = config("ALGORITHM", default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = config("ACCESS_TOKEN_EXPIRE_MINUTES", default=30)
    REFRESH_TOKEN_EXPIRE_DAYS: int = config("REFRESH_TOKEN_EXPIRE_DAYS", default=7)


class DatabaseSettings(BaseSettings):
    pass


class MySQLSettings(DatabaseSettings):
    MYSQL_USER: str = config("MYSQL_USER", default="username")
    MYSQL_PASSWORD: str = config("MYSQL_PASSWORD", default="password")
    MYSQL_SERVER: str = config("MYSQL_SERVER", default="localhost")
    MYSQL_PORT: int = config("MYSQL_PORT", default=3306)
    MYSQL_DB: str = config("MYSQL_DB", default="dbname")
    MYSQL_URI: str = (
        f"{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_SERVER}:{MYSQL_PORT}/{MYSQL_DB}"
    )
    MYSQL_SYNC_PREFIX: str = config("MYSQL_SYNC_PREFIX", default="mysql://")
    MYSQL_ASYNC_PREFIX: str = config("MYSQL_ASYNC_PREFIX", default="mysql+aiomysql://")


class RedisCacheSettings(BaseSettings):
    REDIS_CACHE_HOST: str = config("REDIS_CACHE_HOST", default="localhost")
    REDIS_CACHE_PORT: int = config("REDIS_CACHE_PORT", default=6379)
    REDIS_CACHE_URL: str = f"redis://{REDIS_CACHE_HOST}:{REDIS_CACHE_PORT}"


class DefaultRateLimitSettings(BaseSettings):
    DEFAULT_RATE_LIMIT_LIMIT: int = config("DEFAULT_RATE_LIMIT_LIMIT", default=10)
    DEFAULT_RATE_LIMIT_PERIOD: int = config("DEFAULT_RATE_LIMIT_PERIOD", default=3600)


class EnvironmentOption(Enum):
    LOCAL = "local"
    STAGING = "staging"
    PRODUCTION = "production"


class EnvironmentSettings(BaseSettings):
    ENVIRONMENT: EnvironmentOption = config("ENVIRONMENT", default="local")


class ApplicationSettings(BaseSettings):
    PORT: str = config("PORT", default="8000")
    MICRO_SERVICE_URL_1: str = config("url", default="http://localhost:8000")


class Settings(
    CryptSettings,
    MySQLSettings,
    RedisCacheSettings,
    DefaultRateLimitSettings,
    EnvironmentSettings,
    ApplicationSettings,
):
    pass


settings = Settings()
