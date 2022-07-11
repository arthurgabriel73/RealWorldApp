from functools import lru_cache
from typing import Optional

from fastapi import Depends

from src.exceptions.already_exists import UserAlreadyExists
from src.exceptions.not_found import UserNotFound
from src.modules.users.entities.user import User
from src.modules.users.user_repository import UserRepository
from src.modules.users.repositories.user_repository_impl import (
    user_repository_impl_factory,
)
from src.modules.users.dto.user_dto import UserDTO, UserComplete, UserUpdate


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.__user_repo = user_repository

    async def find_user_by_id(self, user_id: str) -> UserDTO:
        user = await self.__user_repo.find_by_id(user_id)
        if user is None:
            raise UserNotFound(user_id)
        return user

    async def find_user_by_username(self, username: str) -> Optional[User]:
        return self.__user_repo.find_user_by_username(username)

    async def add_user(self, username: str, salted_hash: str) -> str:
        found_username = self.__user_repo.add_user(username, salted_hash)
        if found_username is None:
            raise UserAlreadyExists(username)
        return username

    async def update_user(self, user_id: int, user: UserUpdate) -> UserComplete:
        user = await self.__user_repo.update_user(user_id, user)
        return user


@lru_cache()
def user_service_factory(
        user_repository: UserRepository = Depends(user_repository_impl_factory),
) -> UserService:
    return UserService(user_repository)
