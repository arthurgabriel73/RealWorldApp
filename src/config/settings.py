from datetime import datetime, timedelta
from functools import lru_cache

import pytz
from pydantic import BaseSettings
from sqlalchemy.ext.declarative import declarative_base


class Settings(BaseSettings):
    API_V1_STR: str = '/api/v1'
    DB_URL: str = "postgresql+asyncpg://gcqifvqxeqyaqm:4d6c43629c435e12086a5a0487820f6167bbc85dbdac8ed45a2c6" \
                  "ca7d024e309@ec2-3-208-79-113.compute-1.amazonaws.com:5432/d8v9e5nner8gjt"
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
