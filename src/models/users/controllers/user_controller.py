from fastapi import APIRouter, Depends, status

from src.core.deps import get_current_user, get_session

from src.models.users.entities.user import User
from src.models.users.service.user_service import UserService, user_service_factory
from src.schemas.user_dto import UserDTO, UserSignUp, UserComplete

USERS_URL = '/users'
user_router = APIRouter(
    prefix=USERS_URL, tags=['Users'], dependencies=[Depends(get_session)]
)


@user_router.get("/{user_id}", response_model=UserComplete)
async def get_user(
        user_id: int, user_service: UserService = Depends(user_service_factory)
) -> UserDTO:
    return await user_service.get_user_by_id(user_id)


@user_router.post("/singup", response_model=UserDTO)
async def register_user(
        user: UserSignUp, user_service: UserService = Depends(user_service_factory)
) -> UserDTO:
    return await user_service.register_new_user(user)
