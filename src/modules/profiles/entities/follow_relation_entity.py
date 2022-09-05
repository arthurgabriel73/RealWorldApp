from sqlalchemy import Column, String, ForeignKey, Integer

from config import settings


class FollowRelation(settings.settings_factory().DBBaseModel):
    __tablename__ = 'FOLLOW_RELATION'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, ForeignKey("USERS.username"))
    follower = Column(String, ForeignKey("USERS.username"))
