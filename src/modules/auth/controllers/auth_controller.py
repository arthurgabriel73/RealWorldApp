from fastapi import APIRouter, Body, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from modules.auth.dto.token_dto import Token
from modules.auth.services.auth_service import auth_service_factory
from modules.users.dto.user_dto import IncomingUserDTO, UserDTO, UserLogin, UserComplete
from modules.auth.services.auth_service import AuthService
from modules.users.entities.user_entity import User

AUTH_URL = "/auth"

auth_router = APIRouter(
    prefix=AUTH_URL,
    tags=["Authentication"],
    dependencies=[Depends(auth_service_factory)]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


async def get_user_from_token(
        token: str = Depends(oauth2_scheme),
        auth_service: AuthService = Depends(auth_service_factory),
) -> User:
    return await auth_service.retrieve_user_from_token(token)


@auth_router.post("/signup", response_model=UserComplete)
async def sign_up(
        user: IncomingUserDTO = Body(),
        auth_service: AuthService = Depends(auth_service_factory)
) -> UserDTO:
    return await auth_service.save_user_in_repository(user)


@auth_router.post("/login", response_model=Token)
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        auth_service: AuthService = Depends(auth_service_factory),
) -> Token:
    user = UserLogin(username=form_data.username, password=form_data.password)
    username = await auth_service.authenticate_user(user)
    return await auth_service.create_access_token(username)



