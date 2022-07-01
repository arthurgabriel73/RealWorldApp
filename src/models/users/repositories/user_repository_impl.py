from functools import lru_cache
from typing import Optional, List

from fastapi import Depends

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine


from src.core.database import db_engine_factory

from src.models.users.entities.user import User
from src.models.users.user_repository import UserRepository
from src.schemas.user_dto import UserSignUp, UserDTO


class UserRepositoryImpl(UserRepository):
    def __init__(self, engine: AsyncEngine):
        self.__engine = engine

    async def find_by_id(self, user_id: int) -> UserDTO:
        async with AsyncSession(self.__engine) as session:
            query = select(User).filter(User.id == user_id)
            result = await session.execute(query)
            user: UserDTO = result.scalars().unique().one_or_none()

            return user


@lru_cache
def user_repository_impl_factory(
        db_engine: AsyncEngine = Depends(db_engine_factory),
) -> UserRepositoryImpl:
    return UserRepositoryImpl(db_engine)
