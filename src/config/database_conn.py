from functools import lru_cache
from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine

from src.config.settings import settings_factory, settings
from src.modules.users.entities.user_entity import User

__engine: AsyncEngine = create_async_engine(settings_factory().DB_URL)


Session: AsyncSession = sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession,
    bind=__engine
)


class TokenData(BaseModel):
    username: str | None = None


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


async def get_session() -> Generator:
    session: AsyncSession = Session()

    try:
        yield session
    finally:
        await session.close()


async def get_current_user(
        db: Session = Depends(get_session),
        token: str = Depends(oauth2_scheme)) -> User:

    credential_exception: HTTPException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Authentication failed',
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(
            token,
            settings.TOKEN_SECRET,
            algorithms=[settings.ALGORITHM],
            options={"verify_aud": False}
        )

        username: str = payload.get("sub")
        if username is None:
            raise credential_exception

        token_data: TokenData = TokenData(username=username)
    except JWTError:
        raise credential_exception

    async with db as session:
        query = select(User).filter(User.username == token_data.username)
        result = await session.execute(query)
        user: User = result.scalars().unique().one_or_none()

        if user is None:
            raise credential_exception

        return user


@lru_cache()
def db_engine_factory():
    return __engine
