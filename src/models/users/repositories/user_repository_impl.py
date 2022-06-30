from functools import lru_cache
from typing import Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from src.core.database import db_engine_factory
from src.models.users.entities.user import User
from src.models.users.user_repository import UserRepository


class UserRepositoryImpl(UserRepository):
    def __init__(self, engine: Engine):
        self.__engine = engine

    def find_by_id(self, user_id: str) -> Optional[User]:
        with Session(self.__engine) as session:
            statement = select(User).where(User.id == user_id)
            return session.scalars(statement).one_or_none()


@lru_cache
def user_repository_impl_factory(
        db_engine: Engine = Depends(db_engine_factory),
) -> UserRepositoryImpl:
    return UserRepositoryImpl(db_engine)
