from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from src.config import settings


class User(settings.settings_factory().DBBaseModel):
    __tablename__ = "USERS"
    __table_args__ = {'extend_existing': True}

    id = Column(String, primary_key=True, unique=True)
    username = Column(String, unique=True)
    password_id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    email = Column(String, unique=True)
    bio = Column(String)
    image = Column(String)
    articles = relationship(
        "Article",
        cascade="all,delete-orphan",
        back_populates="author",
        uselist=True,
        lazy="joined"
    )

    password = relationship("Password", back_populates="user")
    followed = relationship("FollowRelation",
                            primaryjoin="and_(User.username==FollowRelation.username,"
                                        "FollowRelation.username==User.username)")
    follower = relationship("FollowRelation",
                            primaryjoin="and_(User.username==FollowRelation.follower,"
                                        "FollowRelation.follower==User.username)")
