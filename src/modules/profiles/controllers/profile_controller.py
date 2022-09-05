from fastapi import APIRouter, Depends

from config.database_conn import get_session
from modules.auth.controllers.auth_controller import get_user_from_token
from modules.profiles.dto.follow_dto import FollowRelationDTO
from modules.profiles.dto.profile_dto import ProfileDTO
from modules.profiles.services.profile_service import profile_service_factory, ProfileService

from modules.users.entities.user_entity import User

PROFILES_URL = '/profiles'

profile_router = APIRouter(
    prefix=PROFILES_URL,
    tags=['Profiles'],
    dependencies=[Depends(get_session)]
)


@profile_router.get("/{username}", response_model=ProfileDTO)
async def get_profile(
        username: str, profile_service: ProfileService = Depends(profile_service_factory)
) -> ProfileDTO | str:
    return await profile_service.get_profile(username)


@profile_router.post("/{username}/follow", response_model=FollowRelationDTO)
async def follow_profile(
        username: str, profile_service: ProfileService = Depends(profile_service_factory),
        logged_user: User = Depends(get_user_from_token)
) -> FollowRelationDTO:
    return await profile_service.follow_username(username, logged_user)


@profile_router.delete("/{username}/unfollow", response_model=FollowRelationDTO)
async def unfollow_profile(
        username: str, profile_service: ProfileService = Depends(profile_service_factory),
        logged_user: User = Depends(get_user_from_token)
) -> FollowRelationDTO:
    return await profile_service.unfollow_username(username, logged_user)

