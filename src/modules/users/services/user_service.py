from functools import lru_cache

from fastapi import Depends

from exceptions.already_exists import UserAlreadyExists
from exceptions.conflict import ConflictOnUpdate
from exceptions.database_exception import IntegrityError, NoResultFound
from exceptions.not_found import UserNotFound
from modules.users.entities.user_entity import User
from modules.users.password_repository import PasswordRepository
from modules.users.repositories.password_repository_impl import password_repository_impl_factory
from modules.users.user_repository import UserRepository
from modules.users.repositories.user_repository_impl import (
    user_repository_impl_factory,
)
from modules.users.dto.user_dto import UserDTO, UserComplete, UserUpdate


class UserService:
    def __init__(self, user_repository: UserRepository, password_repository: PasswordRepository):
        self.__user_repo = user_repository
        self.__password_repo = password_repository

    async def find_user_by_id(self, user_id: str) -> UserDTO:
        user = await self.__user_repo.find_by_id(user_id)
        if user is None:
            raise UserNotFound(user_id)
        return user

    async def find_user_by_username(self, username: str) -> User:
        user = await self.__user_repo.find_user_by_username(username)
        if user is None:
            raise UserNotFound(username)
        return user

    async def add_user(self, username: str) -> User:
        try:
            new_user = await self.__user_repo.add_user(username)
            return new_user

        except IntegrityError:
            raise UserAlreadyExists(username)

    async def update_user(self, user_id: str, user_to_update: UserUpdate, logged_user) -> UserComplete:
        try:
            user = None
            if logged_user.id == user_id:
                user = await self.__user_repo.update_user(user_id, user_to_update)
            return user
        except IntegrityError:
            raise ConflictOnUpdate(user_id)

        except NoResultFound:
            raise UserNotFound(user_id)


@lru_cache()
def user_service_factory(
        user_repository: UserRepository = Depends(user_repository_impl_factory),
        password_repository: PasswordRepository = Depends(password_repository_impl_factory)
) -> UserService:
    return UserService(user_repository, password_repository)
