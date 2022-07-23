"""from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends

from jose import jwt, JWTError

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine

from src.config.settings import settings
from src.config.database_conn import TokenData, Session
from src.modules.auth.current_user_repository import GetCurrentUserRepository
from src.config.database_conn import get_session
from src.modules.users.entities.user_entity import User


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
            self.token,
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

    async with AsyncSession(self.__engine) as session:
        query = select(User).filter(User.username == token_data.username)
        result = await session.execute(query)
        user: User = result.scalars().unique().one_or_none()

        if user is None:
            raise credential_exception

        return user
"""