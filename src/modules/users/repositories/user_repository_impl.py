from functools import lru_cache
from typing import Optional

from fastapi import Depends
import sqlalchemy.exc

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine

from src.config.database_conn import db_engine_factory
from src.config.database_conn import get_session
from src.exceptions.database_exception import IntegrityError, NoResultFound

from src.modules.users.entities.user_entity import User
from src.modules.users.user_repository import UserRepository
from src.modules.users.dto.user_dto import UserDTO, UserUpdate
from src.tools.uuid_tools import generate_uuid


class UserRepositoryImpl(UserRepository):
    def __init__(self, engine: AsyncEngine = Depends(get_session)):
        self.__engine = engine

    async def find_by_id(self, user_id: str) -> UserDTO:
        async with AsyncSession(self.__engine) as session:
            query = select(User).filter(User.id == user_id)
            result = await session.execute(query)
            user: UserDTO = result.scalars().unique().one_or_none()

        return user
# statement = select(User).where(User.id == user_id)
# return session.scalars(statement).one_or_none() > AttributeError: 'coroutine' object has no attribute 'one_or_none'

    async def find_user_by_username(self, username: str) -> User:
        async with AsyncSession(self.__engine) as session:
            try:
                query = select(User).where(User.username == username)
                result = await session.execute(query)
                user: User = result.scalars().unique().one_or_none()
                return user
            except sqlalchemy.exc.NoResultFound:
                raise NoResultFound()

    async def add_user(self, username: str, salted_hash: str) -> str:
        try:
            async with AsyncSession(self.__engine) as session:
                user = User(id=generate_uuid(), username=username)
                session.add(user)
                await session.commit()
                await session.refresh(user)

            return username

        except sqlalchemy.exc.IntegrityError:
            raise IntegrityError()

    async def update_user(self, user_id: int, user: UserUpdate) -> UserUpdate:
        try:
            async with AsyncSession(self.__engine) as session:
                query = select(User).filter(User.id == user_id)
                result = await session.execute(query)
                user_update: UserUpdate = result.scalars().unique().one_or_none()

                if user_update:
                    if user.email:
                        user_update.email = user.email
                    if user.bio:
                        user_update.bio = user.bio
                    if user.image:
                        user_update.image = user.image

                    await session.commit()

        except sqlalchemy.exc.IntegrityError:
            raise IntegrityError()

        return user


@lru_cache
def user_repository_impl_factory(
        db_engine: AsyncEngine = Depends(db_engine_factory),
) -> UserRepositoryImpl:
    return UserRepositoryImpl(db_engine)
