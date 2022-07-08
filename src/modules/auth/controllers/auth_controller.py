from fastapi import APIRouter, Body, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from src.modules.auth.dto.token_dto import Token
from src.modules.auth.services.auth_service import AuthService, auth_service_factory