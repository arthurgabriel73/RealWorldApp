from pydantic import EmailStr

from src.core.configs import settings

from sqlalchemy import Column, Integer, String


class UserModel(settings.DBBaseModel):
    __tablename__ = 'users'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    username: str = Column(String(255), nullable=False, unique=True)
    email: EmailStr = Column(String(255), nullable=False, unique=True)
    password: str = Column(String(255), nullable=False)
    image: str = Column(String(255), nullable=True, unique=False)
    bio: str = Column(String(255), nullable=True, unique=False)
