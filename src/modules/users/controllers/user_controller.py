from fastapi import APIRouter, Depends, Body

from config.database_conn import get_session
from modules.auth.controllers.auth_controller import get_user_from_token
from modules.users.entities.user_entity import User

from modules.users.services.user_service import UserService, user_service_factory
from modules.users.dto.user_dto import UserDTO, UserComplete, UserUpdate

USERS_URL = '/users'

user_router = APIRouter(
    prefix=USERS_URL,
    tags=['Users'],
    dependencies=[Depends(get_session)]
)


@user_router.get("/{user_id}", response_model=UserComplete)
async def get_user(
        user_id: str, user_service: UserService = Depends(user_service_factory)
) -> UserDTO:
    return await user_service.find_user_by_id(user_id)


@user_router.put("/{user_id}", response_model=UserComplete)
async def update_user(
        user_id: str,
        user_to_update: UserUpdate = Body(),
        user_service: UserService = Depends(user_service_factory),
        logged_user: UserUpdate = Depends(get_user_from_token),
) -> UserComplete:
    return await user_service.update_user(user_id, user_to_update, logged_user)
