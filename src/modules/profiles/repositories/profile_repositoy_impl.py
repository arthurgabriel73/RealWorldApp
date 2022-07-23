from functools import lru_cache

from fastapi import Depends, status
from fastapi.openapi.models import Response
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine


from src.config.database_conn import db_engine_factory, get_session
from src.modules.profiles.dto.follow_dto import FollowRelationDTO
from src.modules.profiles.entities.follow_relation_entity import FollowRelation
from src.modules.profiles.profile_repository import ProfileRepository
from src.modules.users.entities.user_entity import User


class ProfileRepositoryImpl(ProfileRepository):
    def __init__(self, engine: AsyncEngine = Depends(get_session)):
        self.__engine = engine

    async def get_followers(self, username: str):
        async with AsyncSession(self.__engine) as session:
            query = select(FollowRelation.follower).where(FollowRelation.username == username)
            result = await session.execute(query)
            followers = result.scalars().unique().all()

            return followers

    async def follow_username(self, username, logged_user) -> FollowRelationDTO:
        async with AsyncSession(self.__engine) as session:
            follow_relation: FollowRelation = FollowRelation(
                username=username,
                follower=logged_user.username
            )

            session.add(follow_relation)
            await session.commit()
            await session.refresh(follow_relation)

            return follow_relation

    async def unfollow_username(self, username, logged_user) -> FollowRelationDTO:
        async with AsyncSession(self.__engine) as session:
            query = select(FollowRelation).where(FollowRelation.username == username)\
                .filter(FollowRelation.follower == logged_user.username)

            result = await session.execute(query)
            follow_relation = result.scalars().unique().one_or_none()

            await session.delete(follow_relation)
            await session.commit()

            return follow_relation


@lru_cache
def profile_repository_impl_factory(
        db_engine: AsyncEngine = Depends(db_engine_factory),
) -> ProfileRepositoryImpl:
    return ProfileRepositoryImpl(db_engine)
