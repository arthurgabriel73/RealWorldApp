from fastapi import APIRouter, Depends

from src.config.database_conn import get_session
from src.modules.profiles.dto.profile_dto import ProfileDTO
from src.modules.profiles.services.profile_service import profile_service_factory, ProfileService

from src.modules.users.dto.user_dto import UserDTO, UserComplete, UserUpdate

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
