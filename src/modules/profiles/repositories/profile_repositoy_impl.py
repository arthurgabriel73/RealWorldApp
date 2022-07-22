from functools import lru_cache

from fastapi import Depends
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine

from src.config.database_conn import db_engine_factory, get_session
from src.modules.profiles.entities.follow_relation_entity import FollowRelation
from src.modules.profiles.profile_repository import ProfileRepository
from src.modules.users.entities.user_entity import User


class ProfileRepositoryImpl(ProfileRepository):
    def __init__(self, engine: AsyncEngine = Depends(get_session)):
        self.__engine = engine

    async def get_followers(self, username: str):
        async with AsyncSession(self.__engine) as session:
            get_uuid = select(User.id).where(User.username == username)
            result = await session.execute(get_uuid)
            uuid = result.scalars().one_or_none()

            query = select(FollowRelation.follower_id).where(FollowRelation.user_id == uuid)
            result = await session.execute(query)  # """PROBLEM"""
            followers = result.scalars().unique().all()

            return followers


@lru_cache
def profile_repository_impl_factory(
        db_engine: AsyncEngine = Depends(db_engine_factory),
) -> ProfileRepositoryImpl:
    return ProfileRepositoryImpl(db_engine)
