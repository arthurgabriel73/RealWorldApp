from pydantic import EmailStr

from src.core.configs import settings

from sqlalchemy import Column, String, Integer


class User(settings.DBBaseModel):
    __tablename__ = 'users'

    id: str = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    username: str = Column(String(255), nullable=False, unique=True)
    email: EmailStr = Column(String(255), nullable=False, unique=True)
    password: str = Column(String(255), nullable=False)
    image: str = Column(String(255), nullable=True, unique=False)
    bio: str = Column(String(255), nullable=True, unique=False)
