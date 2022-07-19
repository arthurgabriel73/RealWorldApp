from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from src.config import settings


class FollowRelation(settings.settings_factory().DBBaseModel):
    __tablename__ = "FOLLOW_RELATION"

    user_id = Column("USER", String, primary_key=True)
    follower_id = Column("FOLLOWER", String)

