from functools import lru_cache

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncEngine

from src.config.database_conn import get_session, db_engine_factory
from src.modules.auth.controllers.auth_controller import get_user_from_token
from src.modules.profiles.dto.follow_dto import FollowRelationDTO
from src.modules.profiles.dto.profile_dto import ProfileDTO
from src.modules.profiles.services.profile_service import profile_service_factory, ProfileService

from src.modules.users.entities.user_entity import User

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


@profile_router.post("/{username}/follow")
async def follow_user(
        username: str, profile_service: ProfileService = Depends(profile_service_factory),
        logged_user: User = Depends(get_user_from_token)
) -> FollowRelationDTO:
    return await profile_service.follow_user(username, logged_user)
