from abc import ABC
from functools import lru_cache

from fastapi import Depends
from sqlalchemy import select
import sqlalchemy.exc
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from src.config.database_conn import get_session, db_engine_factory
from src.exceptions.database_exception import IntegrityError, NoResultFound
from src.modules.auth.entities.password_entity import Password
from src.modules.users.entities.user_entity import User
from src.modules.users.password_repository import PasswordRepository


class PasswordRepositoryImpl(PasswordRepository):

    def __init__(self, engine: AsyncEngine = Depends(get_session)):
        self.__engine = engine

    async def add_password(self, username: str, salted_hash: str) -> str:
        try:
            async with AsyncSession(self.__engine) as session:
                user_id: int = select(User.password_id).where(User.username == username).scalar_subquery()
                salted_hash = Password(id=user_id, salted_hash=salted_hash)
                session.add(salted_hash)
                await session.commit()
                await session.refresh(salted_hash)
            return username

        except sqlalchemy.exc.IntegrityError:
            raise IntegrityError()

    async def get_password(self, password_id: int) -> Password:
        try:
            async with AsyncSession(self.__engine) as session:
                query = select(Password).where(Password.id == password_id)
                result = await session.execute(query)
                password: Password = result.scalars().unique().one_or_none()
            return password
        except sqlalchemy.exc.NoResultFound:
            raise NoResultFound()


@lru_cache
def password_repository_impl_factory(
        db_engine: AsyncEngine = Depends(db_engine_factory),
) -> PasswordRepositoryImpl:
    return PasswordRepositoryImpl(db_engine)
