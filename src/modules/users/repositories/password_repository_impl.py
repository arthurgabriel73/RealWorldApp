from abc import ABC
from functools import lru_cache

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from src.config.database_conn import get_session, db_engine_factory
from src.modules.auth.entities.password_entity import Password
from src.modules.users.entities.user_entity import User
from src.modules.users.password_repository import PasswordRepository


class PasswordRepositoryImpl(PasswordRepository):

    def __init__(self, engine: AsyncEngine = Depends(get_session)):
        self.__engine = engine

    async def add_password(self, username: str, salted_hash: str) -> str:
        async with AsyncSession(self.__engine) as session:
            user_id: int = select(User.password_id).where(User.username == username).scalar_subquery()
            password = Password(id=user_id, user_password=salted_hash)
            session.add(password)
            await session.commit()
            await session.refresh(password)
        return username


@lru_cache
def password_repository_impl_factory(
        db_engine: AsyncEngine = Depends(db_engine_factory),
) -> PasswordRepositoryImpl:
    return PasswordRepositoryImpl(db_engine)
