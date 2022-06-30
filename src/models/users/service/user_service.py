from functools import lru_cache
from typing import List

from fastapi import Depends

from src.core.security import generate_hash_password
from src.exceptions.not_found import user_not_found
from src.models.users.entities.user import User
from src.models.users.user_repository import UserRepository
from src.models.users.repositories.user_repository_impl import (
    user_repository_impl_factory,
)
from src.schemas.user_dto import UserSignUp, UserDto


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.__user_repo = user_repository

    def get_user_by_id(self, user_id: int) -> User:
        user = self.__user_repo.find_by_id(user_id)
        if user is None:
            raise user_not_found()
        return user

    @staticmethod
    def post_user(user: UserSignUp) -> UserDto:
        new_user: User = User(
            username=user.username,
            email=user.email,
            password=generate_hash_password(user.password)
        )
        return new_user


@lru_cache()
def user_service_factory(
        user_repository: UserRepository = Depends(user_repository_impl_factory),
) -> UserService:
    return UserService(user_repository)
