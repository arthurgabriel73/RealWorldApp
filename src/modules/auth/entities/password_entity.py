from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from src.config import settings


class Password(settings.settings_factory().DBBaseModel):
    __tablename__ = 'PASSWORD'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_password = Column(String, unique=True)

    user = relationship("User", back_populates="password", uselist=False)
