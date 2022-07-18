from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from src.config import settings


class FollowRelation(settings.settings_factory().DBBaseModel):
    __tablename__ = "FOLLOW_RELATION"

    user_id = Column("USER", String, ForeignKey("USERS.UUID"), primary_key=True)
    follower_id = Column("FOLLOWER", String, ForeignKey("USERS.UUID"), primary_key=True)

    user = relationship("User", back_populates="followers")
