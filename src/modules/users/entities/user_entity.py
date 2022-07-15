from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from src.config import settings
from src.tools.password_tools import verify_password


class User(settings.settings_factory().DBBaseModel):
    __tablename__ = "USERS"

    id = Column("UUID", String, primary_key=True)
    username = Column(String, unique=True)
    password_id = Column(Integer, ForeignKey("PASSWORD.id"), unique=True)

    password = relationship("Password", back_populates="user")

    def is_password_valid(self, salted_hash: str) -> bool:
        salt, hashed_password = self.salted_hash.split(" ")
        return verify_password(salted_hash, salt, hashed_password)
