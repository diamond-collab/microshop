from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio.session import AsyncSession


from .schemas import LoginResponse, UserLogin
from microshop.api_v1.auth import crud
from microshop.core.models.db_helper import db_helper

router = APIRouter(tags=['Auth'])


@router.post('/login/', response_model=LoginResponse)
async def login(
    user_in: UserLogin,
    session: AsyncSession = Depends(db_helper.get_session),
):
    result = await crud.login_user(user_in=user_in, session=session)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid username or password',
        )

    return result
