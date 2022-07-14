from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from src.config import settings
from src.modules.auth.entities.password_entity import Password
from src.tools.password_tools import verify_password


class User(settings.settings_factory().DBBaseModel):
    __tablename__ = "USERS"

    id: str = Column("UUID", String, primary_key=True, unique=True)
    username = Column("USERNAME", String)
    password_id = Column("PASSWORD_ID", Integer, unique=True)

    def is_password_valid(self, salted_hash: str) -> bool:
        salt, hashed_password = self.salted_hash.split(" ")
        return verify_password(salted_hash, salt, hashed_password)
