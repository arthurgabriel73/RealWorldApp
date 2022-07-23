from fastapi import APIRouter, Body, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from src.config.database_conn import get_current_user
from src.modules.auth.dto.token_dto import Token
from src.modules.auth.services.auth_service import auth_service_factory
from src.modules.users.dto.user_dto import IncomingUserDTO, UserDTO, UserLogin
from src.modules.auth.services.auth_service import AuthService
from src.modules.users.entities.user_entity import User

AUTH_URL = "/auth"

auth_router = APIRouter(
    prefix=AUTH_URL,
    tags=["Authentication"],
    dependencies=[Depends(auth_service_factory)]
)


@auth_router.get('logged', response_model=UserDTO)
def get_logged(logged_user: User = Depends(get_current_user)):
    return logged_user


@auth_router.post("/singup")
async def sign_up(
        user: IncomingUserDTO = Body(),
        auth_service: AuthService = Depends(auth_service_factory)
) -> UserDTO:
    return await auth_service.save_user_in_repository(user)


@auth_router.post("/token", response_model=Token)
async def get_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        auth_service: AuthService = Depends(auth_service_factory),
) -> Token:
    user = UserLogin(username=form_data.username, password=form_data.password)
    username = await auth_service.authenticate_user(user)
    return await auth_service.create_access_token(username)
