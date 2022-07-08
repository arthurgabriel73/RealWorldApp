from functools import lru_cache

from fastapi import Depends
from sqlalchemy.exc import IntegrityError

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine

from src.core.database import db_engine_factory
from src.core.deps import get_session
from src.core.security import generate_hash_password
from src.exceptions.already_owned import email_already_registered


from src.modules.users.entities.user import User
from src.modules.users.user_repository import UserRepository
from src.schemas.user_dto import UserSignUp, UserDTO, UserComplete, UserUpdate


class UserRepositoryImpl(UserRepository):
    def __init__(self, engine: AsyncEngine = Depends(get_session)):
        self.__engine = engine

    async def find_by_id(self, user_id: int) -> UserDTO:
        async with AsyncSession(self.__engine) as session:
            query = select(User).filter(User.id == user_id)
            result = await session.execute(query)
            user: UserDTO = result.scalars().unique().one_or_none()

        return user

# statement = select(User).where(User.id == user_id)
# return session.scalars(statement).one_or_none() > AttributeError: 'coroutine' object has no attribute 'one_or_none'

    async def create_new_user(self, user: UserSignUp) -> UserDTO:
        new_user: User = User(
            username=user.username,
            email=user.email,
            password=generate_hash_password(user.password)
        )

        try:
            async with AsyncSession(self.__engine) as session:
                session.add(new_user)
                await session.commit()

            return user

        except IntegrityError:
            email_already_registered()

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
            email_already_registered()

        return user


@lru_cache
def user_repository_impl_factory(
        db_engine: AsyncEngine = Depends(db_engine_factory),
) -> UserRepositoryImpl:
    return UserRepositoryImpl(db_engine)
