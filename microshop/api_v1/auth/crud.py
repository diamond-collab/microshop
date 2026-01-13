from typing import Any

from sqlalchemy.ext.asyncio.session import AsyncSession

from .jwt import encode_jwt_token, decode_jwt_token
from .schemas import UserLogin, LoginResponse, TokenData
from microshop.api_v1.user import crud, security
from microshop.core.models.user import UserOrm


async def login_user(
    user_in: UserLogin,
    session: AsyncSession,
) -> LoginResponse | None:
    user = await crud.get_user_by_email(session, str(user_in.email))
    if not user:
        return None

    is_valid = security.verify_password(
        password=user_in.password,
        hashed_password=user.hashed_password,
    )
    if not is_valid:
        return None

    user_data: dict[str, Any] = {
        'user_id': user.user_id,
        'username': user.username,
        'email': user.email,
        'role_id': user.role_id,
    }

    token = encode_jwt_token(user_data)

    return LoginResponse(
        user_id=user.user_id,
        username=user.username,
        email=user.email,
        role_id=user.role_id,
        **token,
    )


async def get_current_user(token: 'str', session: AsyncSession) -> UserOrm | None:
    decoded_token: TokenData | None = decode_jwt_token(token=token)
    if not decoded_token:
        return None

    user_id: str = decoded_token.sub
    user = await crud.get_user_by_id(session, int(user_id))
    if not user:
        return None
    return user
