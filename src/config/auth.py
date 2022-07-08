from typing import Optional

from pytz import timezone

from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt

from src.modules.users.entities.user import User
from src.core.configs import settings
from src.core.security import verify_password
from pydantic import EmailStr


oauth2_schema = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/users/login"
)


async def authenticate(email: EmailStr, password: str, db: AsyncSession) -> Optional[User]:
    async with db as session:
        query = select(User).filter(User.email == email)
        result = await session.execute(query)
        user: User = result.scalars().unique().one_or_none()

        if not user:
            return None

        if not verify_password(password, user.password):
            return None

        return user


def _create_token(type_token: str, time_life: timedelta, sub: str) -> str:
    payload = {}
    sp = timezone('America/Sao_paulo')
    expire = datetime.now(tz=sp) + time_life

    payload["type"] = type_token

    payload["exp"] = expire

    payload["iat"] = datetime.now(tz=sp)

    payload["sub"] = str(sub)

    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)


def create_access_token(sub: str) -> str:

    return _create_token(
        type_token='access_token',
        time_life=timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        sub=sub
    )
