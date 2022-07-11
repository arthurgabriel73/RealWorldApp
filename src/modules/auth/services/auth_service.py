from functools import lru_cache

from fastapi import Depends
from jose import jwt

from src.modules.auth.dto.token_dto import Token
from src.config.settings import Settings, settings_factory
from src.exceptions.auth import CouldNotValidate, InvalidPassword, TokenHasExpired
from src.exceptions.not_found import UserNotFound
from src.modules.users.dto.user_dto import IncomingUserDTO, UserDTO, UserComplete
from src.modules.users.entities.user_entity import User
from src.modules.users.services.user_service import UserService, user_service_factory


class AuthService:
    """Implements the actual logic of the authorization process"""

    def __init__(self, user_service: UserService, settings: Settings) -> None:
        self.__user_service = user_service
        self.__settings = settings

    def save_user_in_repository(self, user: IncomingUserDTO) -> None:
        """
    Saves a user in a implementation of the UsersRepository. The password is not saved directly but a string
    with a salt a blank space and the has of the password + salt is used in its place.
    :param user: a user with username and password
    :return: None
    """
        salted_hash = user.get_salted_hash()
        self.__user_service.add_user(user.username, salted_hash)

    def authenticate_user(self, user: IncomingUserDTO) -> str:
        """
       Finds a user using its username than verifies if the passwords are the same.
       :param user: a user with username and password.
       :return: the verified user's username
       """
        stored_user = self.__user_service.find_user_by_username(user.username)
        if stored_user is None:
            raise UserNotFound(user.username)
        is_valid = stored_user.is_password_valid(user.password)
        if not is_valid:
            raise InvalidPassword()
        return user.username

    def create_access_token(self, username: str) -> Token:
        """
     Creates an access token with a given expiration date set in the settings and a given username.
     :param username: a username
     :return: A Token instance.
     """
        data_to_encode = {"sub": username, "exp": self.__settings.get_expiration_date()}
        token = jwt.encode(data_to_encode, self.__settings.TOKEN_SECRET)
        return Token(access_token=token)

    def retrieve_user_from_token(self, token: str) -> UserComplete:
        """
       Decodes the Token, and returns the user that was encoded.
       :param token: A Token object
       :return: a user with username and salt_blank_hash
       """
        try:
            data = jwt.decode(token, self.__settings.TOKEN_SECRET, algorithms=["HS256"])
            stored_user = self.__user_service.find_user_by_username(data.get("sub"))
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
        settings: Settings = Depends(settings_factory)
) -> AuthService:
    return AuthService(user_service, settings)
