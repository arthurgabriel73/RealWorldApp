from fastapi import APIRouter, Depends

from src.config.database_conn import get_session

from src.modules.users.services.user_service import UserService, user_service_factory
from src.modules.users.dto.user_dto import UserDTO, UserComplete, UserUpdate

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
async def update_user(user_id: str, user: UserUpdate, user_service: UserService = Depends(user_service_factory)
                      ) -> UserComplete:
    return await user_service.update_user(user_id, user)
