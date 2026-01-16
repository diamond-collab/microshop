from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, HTTPBearer

from sqlalchemy.ext.asyncio.session import AsyncSession

from .schemas import LoginResponse, UserLogin, ResponseUser, RefreshRequest, RefreshResponse
from .dependencies import current_user
from microshop.api_v1.auth import crud
from microshop.core.models.db_helper import db_helper
from microshop.core.models.user import UserOrm


router = APIRouter(tags=['Auth'])


# oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login/')
oauth2_scheme = HTTPBearer()


@router.post('/login/', response_model=LoginResponse)
async def login(
    user_in: UserLogin,
    session: AsyncSession = Depends(db_helper.get_session),
) -> LoginResponse:
    result = await crud.login_user(user_in=user_in, session=session)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid username or password',
        )

    return result


@router.post('/refresh/', response_model=RefreshResponse)
async def refresh_the_access_token(
    data: RefreshRequest,
    session: AsyncSession = Depends(db_helper.get_session),
):
    result = await crud.refresh_access_token(
        session=session,
        token=data.refresh_token,
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Not authenticated',
        )

    return result


@router.get('/me/', response_model=ResponseUser)
async def get_me(user: UserOrm = Depends(current_user)) -> UserOrm:
    return user
