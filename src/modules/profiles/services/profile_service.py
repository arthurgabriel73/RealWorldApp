from functools import lru_cache

from fastapi import Depends

from src.config.settings import settings_factory, Settings
from src.exceptions.database_exception import IntegrityError
from src.exceptions.not_found import UserNotFound
from src.modules.profiles.dto.follow_dto import FollowRelationDTO
from src.modules.profiles.dto.profile_dto import ProfileDTO
from src.modules.profiles.profile_repository import ProfileRepository
from src.modules.profiles.repositories.profile_repositoy_impl import profile_repository_impl_factory
from src.modules.users.entities.user_entity import User
from src.modules.users.repositories.user_repository_impl import user_repository_impl_factory
from src.modules.users.user_repository import UserRepository


class ProfileService:
    def __init__(self, user_repository: UserRepository, profile_repository: ProfileRepository, settings: Settings):
        self.__user_repo = user_repository
        self.__profile_repo = profile_repository
        self.__settings = settings

    async def get_profile(self, username: str) -> ProfileDTO:
        user = await self.__user_repo.find_user_by_username(username)
        followers = await self.__profile_repo.get_followers(username)

        if followers is None:
            followers = False
        if user is None:
            raise UserNotFound(username)
        else:
            profile: ProfileDTO = ProfileDTO(
                username=username,
                bio=user.bio,
                image=user.image,
                followers=followers
            )

            return profile

    async def follow_username(self, username: str, logged_user: User) -> FollowRelationDTO:
        user = await self.__user_repo.find_user_by_username(username)

        if user is None:
            raise UserNotFound(username)

        username = user.username
        follow_relation = await self.__profile_repo.follow_username(username, logged_user)

        return follow_relation

    async def unfollow_username(self, username: str, logged_user: User) -> FollowRelationDTO:
        user = await self.__user_repo.find_user_by_username(username)

        if user is None:
            raise UserNotFound(username)

        username = user.username
        unfollow_relation = await self.__profile_repo.unfollow_username(username, logged_user)

        return unfollow_relation


@lru_cache
def profile_service_factory(
        user_repository: UserRepository = Depends(user_repository_impl_factory),
        profile_repository: ProfileRepository = Depends(profile_repository_impl_factory),
        settings: Settings = Depends(settings_factory),
) -> ProfileService:
    return ProfileService(user_repository, profile_repository, settings)
