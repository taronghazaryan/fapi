import os

from pydantic import ConfigDict, BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):

    COMPANY_NAME: str = os.getenv('COMPANY_NAME')

    REDIS_HOST: str = os.getenv('REDIS_HOST')
    REDIS_PORT: int = os.getenv('REDIS_PORT')
    REDIS_DB: int = os.getenv('REDIS_DB')

    JWT_SECRET_KEY: str = os.getenv('JWT_SECRET_KEY')
    JWT_ALGORITHM: str = os.getenv('JWT_ALGORITHM')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')
    REFRESH_TOKEN_EXPIRE_DAYS: int = os.getenv('REFRESH_TOKEN_EXPIRE_DAYS')
    # REDIS_PASSWORD

    SUPER_EMAIL: str = os.getenv('SUPER_EMAIL')
    SUPER_EMAIL_PASSWORD: str = os.getenv('SUPER_EMAIL_PASSWORD')

    SMTP_SERVER: str = os.getenv('SMTP_SERVER')
    SMTP_PORT: int = os.getenv('SMTP_PORT')



settings = Settings()
