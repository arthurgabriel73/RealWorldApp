from functools import lru_cache

from fastapi import Depends

from src.exceptions.not_found import user_not_found
from src.modules.users import user_repository
from src.modules.users.entities.user import User
from src.modules.users.user_repository import UserRepository
from src.modules.users.repositories.user_repository_impl import (
    user_repository_impl_factory,
)
from src.schemas.user_dto import UserDTO, UserSignUp, UserComplete, UserUpdate


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.__user_repo = user_repository

    async def get_user_by_id(self, user_id: int) -> UserDTO:
        user = await self.__user_repo.find_by_id(user_id)
        if user is None:
            raise user_not_found()
        return user

    async def register_new_user(self, user: UserSignUp) -> UserDTO:
        return await self.__user_repo.create_new_user(user)

    async def update_user(self, user_id: int, user: UserUpdate) -> UserComplete:
        user = await self.__user_repo.update_user(user_id, user)
        return user


@lru_cache()
def user_service_factory(
        user_repository: UserRepository = Depends(user_repository_impl_factory),
) -> UserService:
    return UserService(user_repository)
