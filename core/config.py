import os

from pydantic import BaseSettings
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class Config(BaseSettings):
    ENV: str = os.getenv("ENV", "development")
    DEBUG: bool = os.getenv("DEBUG", True)
    APP_HOST: str = os.getenv("APP_HOST", "0.0.0.0")
    APP_PORT: int = os.getenv("APP_PORT", 8000)
    MEDIA_URL: str = os.getenv("MEDIA_URL", "./media")

    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")

    SENTRY_DSN: str = os.getenv("SENTRY_DSN", "")

    CELERY_BROKER_URL: str = f"pyamqp://{os.getenv('RABBITMQ_DEFAULT_USER')}:" \
                             f"{os.getenv('RABBITMQ_DEFAULT_PASS')}@{os.getenv('RABBITMQ_HOST')}//"
    CELERY_BACKEND_URL: str = f"rpc://{os.getenv('RABBITMQ_DEFAULT_USER')}:" \
                              f"{os.getenv('RABBITMQ_DEFAULT_PASS')}@{os.getenv('RABBITMQ_HOST')}//"

    MONGO_HOST: str = os.getenv("MONGO_HOST", "mongo")
    MONGO_PORT: int = os.getenv("MONGO_PORT", 27017)

    REDIS_HOST: str = os.getenv("REDIS_HOST", "redis")
    REDIS_PORT: int = os.getenv("REDIS_PORT", 6379)

    SMTP_SERVER: str = os.getenv("SMTP_SERVER", "")
    SMTP_PORT: int = os.getenv("SMTP_PORT", 0)
    SMTP_USERNAME: str = os.getenv("SMTP_USERNAME", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")


class DevelopmentConfig(Config):
    WRITER_DB_URL: str = f"postgresql+asyncpg://{os.getenv('POSTGRES_USER_DEV')}:" \
                         f"{os.getenv('POSTGRES_PASSWORD_DEV')}@" \
                         f"{os.getenv('POSTGRES_HOST_DEV')}:" \
                         f"{os.getenv('POSTGRES_PORT_DEV')}/{os.getenv('POSTGRES_DB_DEV')}"
    READER_DB_URL: str = f"postgresql+asyncpg://{os.getenv('POSTGRES_USER_DEV')}:" \
                         f"{os.getenv('POSTGRES_PASSWORD_DEV')}@" \
                         f"{os.getenv('POSTGRES_HOST_DEV')}:" \
                         f"{os.getenv('POSTGRES_PORT_DEV')}/{os.getenv('POSTGRES_DB_DEV')}"
    SYNC_WRITER_DB_URL: str = f"postgresql://{os.getenv('POSTGRES_USER_DEV')}:" \
                              f"{os.getenv('POSTGRES_PASSWORD_DEV')}@" \
                              f"{os.getenv('POSTGRES_HOST_DEV')}:" \
                              f"{os.getenv('POSTGRES_PORT_DEV')}/{os.getenv('POSTGRES_DB_DEV')}"
    # ELASTICSEARCH_HOSTS: str = f"{os.getenv('ELASTICSEARCH_HOSTS', 'elasticsearch')}"
    # ELASTICSEARCH_PORT: str = f"{os.getenv('ELASTICSEARCH_PORT', 9200)}"
    # ELASTICSEARCH_INDEX: str = f"{os.getenv('ELASTICSEARCH_INDEX', 'events')}"


class LocalConfig(Config):
    WRITER_DB_URL: str = f"postgresql+asyncpg://{os.getenv('POSTGRES_USER_LOCAL')}:" \
                         f"{os.getenv('POSTGRES_PASSWORD_LOCAL')}@" \
                         f"{os.getenv('POSTGRES_HOST_LOCAL')}:" \
                         f"{os.getenv('POSTGRES_PORT_LOCAL')}/{os.getenv('POSTGRES_DB_LOCAL')}"
    READER_DB_URL: str = f"postgresql+asyncpg://{os.getenv('POSTGRES_USER_LOCAL')}:" \
                         f"{os.getenv('POSTGRES_PASSWORD_LOCAL')}@" \
                         f"{os.getenv('POSTGRES_HOST_LOCAL')}:" \
                         f"{os.getenv('POSTGRES_PORT_LOCAL')}/{os.getenv('POSTGRES_DB_LOCAL')}"
    SYNC_WRITER_DB_URL: str = f"postgresql://{os.getenv('POSTGRES_USER_LOCAL')}:" \
                              f"{os.getenv('POSTGRES_PASSWORD_LOCAL')}@" \
                              f"{os.getenv('POSTGRES_HOST_LOCAL')}:" \
                              f"{os.getenv('POSTGRES_PORT_LOCAL')}/{os.getenv('POSTGRES_DB_LOCAL')}"
    # ELASTICSEARCH_HOSTS: str = f"{os.getenv('ELASTICSEARCH_HOSTS', 'elasticsearch')}"
    # ELASTICSEARCH_PORT: str = f"{os.getenv('ELASTICSEARCH_PORT', 9200)}"
    # ELASTICSEARCH_INDEX: str = f"{os.getenv('ELASTICSEARCH_INDEX', 'events')}"


class TestConfig(Config):
    TESTING: bool = True
    WRITER_DB_URL = f"postgresql+asyncpg://{os.getenv('POSTGRES_USER_TEST')}:" \
                    f"{os.getenv('POSTGRES_PASSWORD_TEST')}@" \
                    f"{os.getenv('POSTGRES_HOST_TEST')}:" \
                    f"{os.getenv('POSTGRES_PORT_TEST')}/{os.getenv('POSTGRES_DB_TEST')}"
    READER_DB_URL = f"postgresql+asyncpg://{os.getenv('POSTGRES_USER_TEST')}:" \
                    f"{os.getenv('POSTGRES_PASSWORD_TEST')}@" \
                    f"{os.getenv('POSTGRES_HOST_TEST')}:" \
                    f"{os.getenv('POSTGRES_PORT_TEST')}/{os.getenv('POSTGRES_DB_TEST')}"
    SYNC_WRITER_DB_URL: str = f"postgresql://{os.getenv('POSTGRES_USER_TEST')}:" \
                              f"{os.getenv('POSTGRES_PASSWORD_TEST')}@" \
                              f"{os.getenv('POSTGRES_HOST_TEST')}:" \
                              f"{os.getenv('POSTGRES_PORT_TEST')}/{os.getenv('POSTGRES_DB_TEST')}"

    ELASTICSEARCH_HOSTS: str = f"213213"
    ELASTICSEARCH_PORT: str = f"{os.getenv('ELASTICSEARCH_PORT_TEST')}"
    ELASTICSEARCH_INDEX: str = f"{os.getenv('ELASTICSEARCH_INDEX_TEST')}"


class ProductionConfig(Config):
    DEBUG: bool = False
    WRITER_DB_URL: str = f"postgresql+asyncpg://{os.getenv('POSTGRES_USER_PROD')}:" \
                         f"{os.getenv('POSTGRES_PASSWORD_PROD')}@" \
                         f"{os.getenv('POSTGRES_HOST_PROD')}:" \
                         f"{os.getenv('POSTGRES_PORT_PROD')}/{os.getenv('POSTGRES_DB_PROD')}"
    READER_DB_URL: str = f"postgresql+asyncpg://{os.getenv('POSTGRES_USER_PROD')}:" \
                         f"{os.getenv('POSTGRES_PASSWORD_PROD')}@" \
                         f"{os.getenv('POSTGRES_HOST_PROD')}:" \
                         f"{os.getenv('POSTGRES_PORT_PROD')}/{os.getenv('POSTGRES_DB_PROD')}"
    SYNC_WRITER_DB_URL: str = f"postgresql://{os.getenv('POSTGRES_USER_PROD')}:" \
                              f"{os.getenv('POSTGRES_PASSWORD_PROD')}@" \
                              f"{os.getenv('POSTGRES_HOST_PROD')}:" \
                              f"{os.getenv('POSTGRES_PORT_PROD')}/{os.getenv('POSTGRES_DB_PROD')}"


def get_config():
    env = os.getenv("ENV", "local")
    config_type = {
        "dev": DevelopmentConfig(),
        "local": LocalConfig(),
        "prod": ProductionConfig(),
        "test": TestConfig(),
    }
    return config_type[env]


config: Config = get_config()
