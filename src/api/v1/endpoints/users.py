from typing import List

from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr
from sqlalchemy.exc import IntegrityError

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from starlette.responses import JSONResponse

from src.core.auth import authenticate, create_access_token
from src.core.security import generate_hash_password
from src.models.user_model import UserModel
from src.schemas.user_dto import User, UserSignUp, UserUpdate, UserComplete
from src.core.deps import get_session, get_current_user

router = APIRouter()


# GET LOGGED
@router.post('logged', response_model=User)
def get_logged(logged_user: UserModel = Depends(get_current_user)):
    return logged_user


# POST USER - singup
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=User)
async def singup(user: UserSignUp, db: AsyncSession = Depends(get_session)):
    new_user: UserModel = UserModel(
        username=user.username,
        email=user.email,
        password=generate_hash_password(user.password)
    )

    async with db as session:
        try:
            session.add(new_user)
            await session.commit()

            return new_user
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                detail='This username/email is already owned.')


# GET USERS
@router.get('/', response_model=List[User])
async def get_users(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UserModel)
        result = await session.execute(query)
        users: List[User] = result.scalars().unique().all()

        return users


# GET USER by id
@router.get('/{user_id}', response_model=UserComplete, status_code=status.HTTP_200_OK)
async def get_user(user_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UserModel).filter(UserModel.id == user_id)
        result = await session.execute(query)
        user: User = result.scalars().unique().one_or_none()

        if user:
            return user
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found.')


# PUT USER - update user
@router.put('{user_id}', response_model=UserComplete, status_code=status.HTTP_202_ACCEPTED)
async def update_user(user_id: int, user: UserUpdate, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UserModel).filter(UserModel.id == user_id)
        result = await session.execute(query)
        updated_user: UserModel = result.scalars().unique().one_or_none()

        if updated_user:
            if user.username:
                updated_user.username = user.username
            if user.email:
                updated_user.email = user.email
            if user.password:
                updated_user.password = generate_hash_password(user.password)
            if user.image:
                updated_user.image = user.image
            if user.bio:
                updated_user.bio = user.bio

            await session.commit()

            return updated_user
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found.')


# DELETE USER
@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UserModel).filter(UserModel.id == user_id)
        result = await session.execute(query)
        user_del: User = result.scalars().unique().one_or_none()

    if user_del:
        await session.delete(user_del)
        await session.commit()

        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found.')


# POST LOGIN
@router.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    user = await authenticate(email=EmailStr(form_data.username), password=form_data.password, db=db)

    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid access data.")

    return JSONResponse(content={'access_token': create_access_token(sub=str(user.id)), "token_type": "bearer"},
                        status_code=status.HTTP_200_OK)


# POST FOLLOW User
@router.post('/{user_id}/follow', status_code=status.HTTP_202_ACCEPTED)
async def follow_user(user_id: int, db: AsyncSession = Depends(get_session),
                      logged_user: UserModel = Depends(get_current_user)):
    async with db as session:
        query = select(UserModel).filter(UserModel.id == user_id)
        result = await session.execute(query)
        user_to_follow = result.scalars().unique().one_or_none()

        if user_to_follow:
            logged_user.following.append(user_id)

            return user_to_follow

        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
