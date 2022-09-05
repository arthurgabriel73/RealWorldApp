from functools import lru_cache

import sqlalchemy
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine

from exceptions.not_found import FollowRelationNotFound
from config.database_conn import db_engine_factory, get_session
from modules.profiles.dto.follow_dto import FollowRelationDTO
from modules.profiles.entities.follow_relation_entity import FollowRelation
from modules.profiles.profile_repository import ProfileRepository


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
            query = select(FollowRelation).where(FollowRelation.username == username)\
                .filter(FollowRelation.follower == logged_user.username)
            result = await session.execute(query)
            relation_exists = result.scalars().one_or_none()

            follow_relation: FollowRelation = FollowRelation(
                username=username,
                follower=logged_user.username

            )
            if relation_exists is None:
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
            try:
                await session.delete(follow_relation)
                await session.commit()

                return follow_relation

            except sqlalchemy.orm.exc.UnmappedInstanceError:
                raise FollowRelationNotFound()


@lru_cache
def profile_repository_impl_factory(
        db_engine: AsyncEngine = Depends(db_engine_factory),
) -> ProfileRepositoryImpl:
    return ProfileRepositoryImpl(db_engine)
