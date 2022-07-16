from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from src.config import settings


class Password(settings.settings_factory().DBBaseModel):
    __tablename__ = 'PASSWORD'

    id = Column(Integer, ForeignKey("USERS.password_id"), primary_key=True)
    user_password = Column(String, unique=True)

    user = relationship("User", back_populates="password", uselist=False)
