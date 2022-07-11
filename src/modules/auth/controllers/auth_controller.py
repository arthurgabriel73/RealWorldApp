from fastapi import APIRouter, Body, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from src.modules.auth.dto.token_dto import Token
from src.modules.auth.services.auth_service import AuthService, auth_service_factory
from src.modules.users.dto.user_dto import IncomingUserDTO, UserDTO


AUTH_URL = "/auth"

auth_router = APIRouter(
    prefix=AUTH_URL,
    tags=["Authentication"],
    dependencies=[Depends(auth_service_factory)]
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def get_user_from_token(
        token: str = Depends(oauth2_scheme),
        auth_service: AuthService = Depends(auth_service_factory)
) -> UserDTO:
    return auth_service.retrieve_user_from_token(token)


@auth_router.post("/singup")
async def sign_up(
        user: IncomingUserDTO = Body(),
        auth_service: AuthService = Depends(auth_service_factory)
) -> None:
    auth_service.save_user_in_repository(user)


@auth_router.post("/token", response_model=Token)
async def get_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        auth_service: AuthService = Depends(auth_service_factory),
) -> Token:
    user = IncomingUserDTO(username=form_data.username, passoword=form_data.password)
    username = auth_service.authenticate_user(user)
    return auth_service.create_access_token(username)

"""
sing up, get access token"""