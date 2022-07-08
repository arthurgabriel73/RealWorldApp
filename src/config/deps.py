from typing import Generator

from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.core.auth import oauth2_schema
from src.core.configs import settings
from src.core.database import Session
from src.modules.users.entities.user import User


class TokenData(BaseModel):
    username: str | None = None


async def get_session() -> Generator:
    session: AsyncSession = AsyncSession()

    try:
        yield session
    finally:
        await session.close()


async def get_current_user(
        db: Session = Depends(get_session),
        token: str = Depends(oauth2_schema)) -> User:

    credential_exception: HTTPException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Authentication failed',
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
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
        query = select(User).filter(User.id == int(token_data.username))
        result = await session.execute(query)
        user: User = result.scalars().unique().one_or_none()

        if user is None:
            raise credential_exception

        return user
