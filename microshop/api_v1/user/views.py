from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio.session import AsyncSession

from . import crud
from .schemas import UserCreate, UpdateUser, UserResponse
from microshop.core.models.db_helper import db_helper


router = APIRouter(tags=['User'])


@router.post('/', response_model=UserResponse)
async def create_user(user_in: UserCreate, session: AsyncSession = Depends(db_helper.get_session)):
    return await crud.create_user(session=session, user_in=user_in)


@router.get('/{user_id}/', response_model=UserResponse)
async def get_user_by_id(user_id: int, session: AsyncSession = Depends(db_helper.get_session)):
    user = await crud.get_user_by_id(session=session, user_id=user_id)

    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f'User with id {user_id} not found')

    return user


@router.patch('/{user_id}/', response_model=UserResponse)
async def update_data_user(
    user_id: int, data: UpdateUser, session: AsyncSession = Depends(db_helper.get_session)
):
    update_data = await crud.update_data_user(session=session, user_id=user_id, data=data)

    if update_data is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f'User with id {user_id} not found')

    return update_data


@router.delete('/{user_id}/', status_code=status.HTTP_204_NO_CONTENT)
async def delete_data_user(user_id: int, session: AsyncSession = Depends(db_helper.get_session)):
    result = await crud.delete_user(session=session, user_id=user_id)
    if result is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f'User with id {user_id} not found')
