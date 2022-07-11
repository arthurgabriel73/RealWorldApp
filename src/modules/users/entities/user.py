from pydantic import EmailStr

from src.config.settings import settings_factory

from sqlalchemy import Column, String, Integer

from src.tools.password_tools import verify_password


class User(settings_factory().DBBaseModel):
    __tablename__ = 'users'

    id: str = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    username: str = Column(String(255), nullable=False, unique=True)
    email: EmailStr = Column(String(255), nullable=False, unique=True)
    salted_hash: str = Column("PASSWORD", String)
    image: str = Column(String(255), nullable=True, unique=False)
    bio: str = Column(String(255), nullable=True, unique=False)

    def is_password_valid(self, salted_hash: str) -> bool:
        salt, hashed_password = self.salted_hash.split(" ")
        return verify_password(salted_hash, salt, hashed_password)
