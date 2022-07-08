from functools import lru_cache

from fastapi import Depends
from jose import jwt

from src.modules.auth.dto.token_dto import Token
from src.config.settings import Settings, settings_factory
from src.exceptions.auth import CouldNotValidate, InvalidPassword, TokenHasExpired
from src.exceptions.not_found import UserNotFound
from src.modules.users.dto.incoming_user_dto import IncomingUserDTO
from src.modules.users.entities.user_entity import