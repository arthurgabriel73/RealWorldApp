from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from src.config import settings
from src.tools.password_tools import verify_password


class User(settings.settings_factory().DBBaseModel):
    __tablename__ = "USERS"

    id = Column("UUID", String, primary_key=True, unique=True)
    username = Column(String, unique=True)
    password_id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    email = Column(String, unique=True)
    bio = Column(String)
    image = Column(String)

    password = relationship("Password", back_populates="user")
    followed = relationship("FollowRelation",
                            primaryjoin="and_(User.username==FollowRelation.username,"
                                        "FollowRelation.username==User.username)")
    follower = relationship("FollowRelation",
                            primaryjoin="and_(User.username==FollowRelation.follower,"
                                        "FollowRelation.follower==User.username)")
