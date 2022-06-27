from pydantic import BaseSettings
from sqlalchemy.ext.declarative import declarative_base


class Settings(BaseSettings):
    API_V1_STR: str = '/api/v1'
    DB_URL: str = "postgresql+asyncpg://postgres:c4c232a4@localhost:5432/real_world"
    DBBaseModel: str = declarative_base()


class Config:
    case_sensitive = True


settings: Settings = Settings()
