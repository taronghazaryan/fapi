from dataclasses import Field
from datetime import datetime
from pathlib import Path

from pydantic import ConfigDict, BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseModel):

    REDIS_HOST: str = ConfigDict()
    REDIS_PORT: int = ConfigDict()
    REDIS_DB: int = ConfigDict()

    JWT_SECRET_KEY: str = ConfigDict()
    JWT_ALGORITHM: str = ConfigDict()
    ACCESS_TOKEN_EXPIRE_MINUTES: int = ConfigDict()
    REFRESH_TOKEN_EXPIRE_DAYS: int = ConfigDict()
    # REDIS_PASSWORD



settings = Settings()
