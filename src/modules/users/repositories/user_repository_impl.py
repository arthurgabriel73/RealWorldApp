from functools import lru_cache
from typing import Optional

from fastapi import Depends
from sqlalchemy.exc import IntegrityError

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine

from src.config.database_conn import db_engine_factory
from src.config.database_conn import get_session
from src.exceptions.already_exists import UserAlreadyExists

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

    async def find_user_by_username(self, username: str) -> Optional[User]:
        async with AsyncSession(self.__engine) as session:
            query = select(User).where(User.username == username)
            result = await session.execute(query)

        return result.scalars().unique().one_or_none()

    async def add_user(self, username: str) -> Optional[str]:
        try:
            async with AsyncSession(self.__engine) as session:
                user = User(id=generate_uuid(), username=username)
                stored_user = await self.find_user_by_username(user.username)
                if stored_user is not None:
                    return None

                session.add(user)
                await session.commit()
                await session.refresh(user)

            return username

        except IntegrityError:
            UserAlreadyExists(user.username)

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

        except IntegrityError:
            UserAlreadyExists(user.username)

        return user


@lru_cache
def user_repository_impl_factory(
        db_engine: AsyncEngine = Depends(db_engine_factory),
) -> UserRepositoryImpl:
    return UserRepositoryImpl(db_engine)
