import os

from pydantic import BaseSettings


class Config(BaseSettings):
    ENV: str = "development"
    DEBUG: bool = True
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    WRITER_DB_URL: str = f"mysql+aiomysql://fastapi:fastapi@localhost:3306/fastapi"
    READER_DB_URL: str = f"mysql+aiomysql://fastapi:fastapi@localhost:3306/fastapi"
    JWT_SECRET_KEY: str = "fastapi"
    JWT_ALGORITHM: str = "HS256"
    SENTRY_DSN: str = os.getenv("SENTRY_DSN", "")
    CELERY_BROKER_URL: str = "pyamqp://guest@localhost//"
    CELERY_BACKEND_URL: str = "rpc://guest@localhost//"
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    SMTP_SERVER: str = ""
    SMTP_PORT: int = None
    SMTP_USERNAME: str = ""
    SMTP_PASSWORD: str = ""


class DevelopmentConfig(Config):
    WRITER_DB_URL: str = f"mysql+aiomysql://root:fastapi@db:3306/fastapi"
    READER_DB_URL: str = f"mysql+aiomysql://root:fastapi@db:3306/fastapi"
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379


class LocalConfig(Config):
    WRITER_DB_URL: str = f"postgresql+asyncpg://postgres:password@localhost:1/name_databas"
    READER_DB_URL: str = f"postgresql+asyncpg://postgres:password@localhost:1/name_databas"
    SYNC_WRITER_DB_URL: str = f"postgresql://postgres:password@localhost:1/name_databas"


class ProductionConfig(Config):
    DEBUG: str = False
    WRITER_DB_URL: str = f"mysql+aiomysql://fastapi:fastapi@localhost:3306/prod"
    READER_DB_URL: str = f"mysql+aiomysql://fastapi:fastapi@localhost:3306/prod"


def get_config():
    env = os.getenv("ENV", "local")
    config_type = {
        "dev": DevelopmentConfig(),
        "local": LocalConfig(),
        "prod": ProductionConfig(),
    }
    return config_type[env]


config: Config = get_config()
