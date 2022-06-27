from typing import List

from fastapi import APIRouter, status, Depends, HTTPException, Response
from sqlalchemy.exc import IntegrityError

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.user_model import UserModel
from schemas.user_schema import UserSchemaBase, UserSchemaSignUp, UserSchemaUpdate
from core.deps import get_session


router = APIRouter()


# POST USER - singup
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserSchemaBase)
async def singup(user: UserSchemaSignUp, db: AsyncSession = Depends(get_session)):
    new_user: UserModel = UserModel(
        username=user.username,
        email=user.email,
        password=user.password)

    async with db as session:
        try:
            session.add(new_user)
            await session.commit()

            return new_user
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                detail='This username/email is already owned.')


# GET USERS
@router.get('/', response_model=List[UserSchemaBase])
async def get_users(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UserModel)
        result = await session.execute(query)
        users: List[UserSchemaBase] = result.scalars().unique().all()

        return users


# GET USER by id
@router.get('/{user_id}', response_model=UserSchemaBase, status_code=status.HTTP_200_OK)
async def get_user(user_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UserModel).filter(UserModel.id == user_id)
        result = await session.execute(query)
        user: UserSchemaBase = result.scalars().unique().one_or_none()

        if user:
            return user
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found.')


# PUT USER - update user
@router.put('{user_id}', response_model=UserSchemaBase, status_code=status.HTTP_202_ACCEPTED)
async def update_user(user_id: int, user: UserSchemaUpdate, db: AsyncSession = Depends(get_session)):
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
                updated_user.password = user.password

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
        user_del: UserSchemaBase = result.scalars().unique().one_or_none()

    if user_del:
        await session.delete(user_del)
        await session.commit()

        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found.')
