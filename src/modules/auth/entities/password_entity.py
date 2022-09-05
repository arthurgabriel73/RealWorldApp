from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from config import settings
from tools.password_tools import verify_password


class Password(settings.settings_factory().DBBaseModel):
    __tablename__ = 'PASSWORD'

    id = Column(Integer, ForeignKey("USERS.password_id"), primary_key=True)
    salted_hash = Column(String, unique=True)

    user = relationship("User", back_populates="password", uselist=False)

    def is_password_valid(self, salted_hash: str) -> bool:
        salt, hashed_password = self.salted_hash.split(" ")
        return verify_password(salted_hash, salt, hashed_password)
