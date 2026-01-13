from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, HTTPBearer

from sqlalchemy.ext.asyncio.session import AsyncSession

from .schemas import LoginResponse, UserLogin, ResponseUser
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


@router.get('/me/', response_model=ResponseUser)
async def get_me(
    token=Depends(oauth2_scheme),
    session: AsyncSession = Depends(db_helper.get_session),
) -> UserOrm:
    raw_token = token.credentials
    result = await crud.get_current_user(token=raw_token, session=session)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid credentials',
        )

    return result
