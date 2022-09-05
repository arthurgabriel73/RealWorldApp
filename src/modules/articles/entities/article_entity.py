from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from config import settings


class Article(settings.settings_factory().DBBaseModel):
    __tablename__ = 'ARTICLES'

    id = Column(Integer, primary_key=True, autoincrement=True)
    slug = Column(String)
    title = Column(String(256), unique=True)
    description = Column(String)
    body = Column(String)
    author_id = Column(String, ForeignKey("USERS.id"), primary_key=True)

    author = relationship("User", back_populates='articles',
                          lazy='joined')
