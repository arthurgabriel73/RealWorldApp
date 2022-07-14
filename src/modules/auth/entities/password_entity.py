from sqlalchemy import Column, Integer, String, ForeignKey

from src.config import settings


class Password(settings.settings_factory().DBBaseModel):
    __tablename__ = 'PASSWORD'

    id = Column(Integer, ForeignKey("USERS.PASSWORD_ID"), primary_key=True, autoincrement=True)
    password = Column(String)
