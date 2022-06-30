from pydantic import BaseSettings
from sqlalchemy.ext.declarative import declarative_base


class Settings(BaseSettings):
    API_V1_STR: str = '/api/v1'
    DB_URL: str = "postgresql+asyncpg://postgres:c4c232a4@localhost:5432/real_world_app"
    DBBaseModel = declarative_base()

    JWT_SECRET: str = '-0sG5ezMEHZ9zu3g7pbCIQcK1Dhg5I4Y3SEiq0OB1F4'
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 180


class Config:
    case_sensitive = True


settings: Settings = Settings()
