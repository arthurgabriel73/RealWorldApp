from functools import lru_cache

from fastapi import Depends
from jose import jwt

from src.exceptions.already_exists import UserAlreadyExists
from src.exceptions.database_exception import IntegrityError
from src.modules.auth.dto.token_dto import Token
from src.config.settings import Settings, settings_factory
from src.exceptions.auth import CouldNotValidate, InvalidPassword, TokenHasExpired
from src.exceptions.not_found import UserNotFound
from src.modules.users.dto.user_dto import IncomingUserDTO, UserDTO, UserComplete
from src.modules.users.password_repository import PasswordRepository
from src.modules.users.repositories.password_repository_impl import password_repository_impl_factory
from src.modules.users.services.user_service import UserService, user_service_factory


class AuthService:

    def __init__(self, user_service: UserService, password_repository: PasswordRepository, settings: Settings) -> None:
        self.__password_repository = password_repository
        self.__user_service = user_service
        self.__settings = settings

    async def save_user_in_repository(self, user: IncomingUserDTO):
        salted_hash = user.get_salted_hash()
        try:
            await self.__user_service.add_user(user.username, salted_hash)
            return await self.__password_repository.add_password(user.username, salted_hash)

        except IntegrityError:
            UserAlreadyExists(user.username)

    async def authenticate_user(self, user: IncomingUserDTO) -> str:
        stored_user = await self.__user_service.find_user_by_username(user.username)
        if stored_user is None:
            raise UserNotFound(user.username)

        is_valid = stored_user.is_password_valid(user.password)

        if not is_valid:
            raise InvalidPassword()
        return user.username

    def create_access_token(self, username: str) -> Token:
        data_to_encode = {"sub": username, "exp": self.__settings.get_expiration_date()}
        token = jwt.encode(data_to_encode, self.__settings.TOKEN_SECRET)
        return Token(access_token=token)

    async def retrieve_user_from_token(self, token: str) -> UserComplete:
        try:
            data = jwt.decode(token, self.__settings.TOKEN_SECRET, algorithms=["HS256"])
            stored_user = await self.__user_service.find_user_by_username(data.get("sub"))
            if stored_user is None:
                raise CouldNotValidate()
            return stored_user
        except jwt.ExpiredSignatureError:
            raise TokenHasExpired()
        except Exception:
            raise CouldNotValidate()


@lru_cache
def auth_service_factory(
        user_service: UserService = Depends(user_service_factory),
        settings: Settings = Depends(settings_factory),
        password_repository: PasswordRepository = Depends(password_repository_impl_factory)
) -> AuthService:
    return AuthService(user_service, password_repository, settings)
