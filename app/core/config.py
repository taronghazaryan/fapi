import redis
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    COMPANY_NAME: str

    SECRET_KEY: str

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    # REDIS_PASSWORD

    SUPER_EMAIL: str
    SUPER_EMAIL_PASSWORD: str

    SMTP_SERVER: str
    SMTP_PORT: int

    EXCLUDED_PATHS: str

    model_config = SettingsConfigDict(env_file='.env')



settings = Settings()

redis_instance = redis.StrictRedis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            decode_responses=True
        )
