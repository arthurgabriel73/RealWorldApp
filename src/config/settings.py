from datetime import datetime, timedelta
from functools import lru_cache

import pytz
from pydantic import BaseSettings
from sqlalchemy.ext.declarative import declarative_base


class Settings(BaseSettings):
    API_V1_STR: str = '/api/v1'
    DB_URL: str = "postgresql+asyncpg://postgres:c4c232a4@localhost:5432/real_world_app"
    DBBaseModel = declarative_base()

    TOKEN_SECRET: str = '-0sG5ezMEHZ9zu3g7pbCIQcK1Dhg5I4Y3SEiq0OB1F4'
    ALGORITHM: str = 'HS256'
    MINUTES_FOR_TOKEN_EXPIRATION: int = 180

    def get_expiration_date(self) -> datetime:
        now = datetime.now(pytz.timezone("America/Sao_Paulo"))
        return now + timedelta(minutes=self.MINUTES_FOR_TOKEN_EXPIRATION)

    def __hash__(self):
        return hash(str(self))


class Config:
    case_sensitive = True


settings: Settings = Settings()


@lru_cache
def settings_factory() -> Settings:
    return Settings()
