from fastapi import APIRouter, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.deps import get_current_user, get_session
from src.exceptions.already_owned import email_already_registered
from src.models.users.entities.user import User
from src.models.users.service.user_service import UserService, user_service_factory
from src.schemas.user_dto import UserDto, UserSignUp

USERS_URL = '/users'
user_router = APIRouter(
    prefix=USERS_URL, tags=['Users'], dependencies=[Depends(get_session)]
)


@user_router.get("/{user_id}")
async def get_user(
        user_id: int, user_service: UserService = Depends(user_service_factory)
) -> User:
    return user_service.get_user_by_id(user_id)


@user_router.post("/users", response_model=UserDto)
async def post_user(
        user: UserSignUp, db: AsyncSession = Depends(get_session),
        user_service: UserService = Depends(user_service_factory)):
    async with db as session:  # ERRADO, precisar estar no user_repository
        try:
            session.add(user_service.post_user(user))
            await session.commit()

            return user_service.post_user(user)
        except IntegrityError:
            email_already_registered()
