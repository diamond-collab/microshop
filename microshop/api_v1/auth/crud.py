from typing import Any

from sqlalchemy.ext.asyncio.session import AsyncSession

from .jwt import encode_access_token, encode_refresh_token, decode_refresh_token
from .schemas import (
    UserLogin,
    LoginResponse,
    RefreshResponse,
    PublicResponse,
)
from microshop.api_v1.user import crud, security


async def login_user(
    user_in: UserLogin,
    session: AsyncSession,
) -> tuple[PublicResponse, LoginResponse] | None:
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

    access_token = encode_access_token(user_data)
    refresh_token = encode_refresh_token(user_data)

    login_response = LoginResponse(
        refresh_token=refresh_token.get('refresh_token'),
    )

    public_response = PublicResponse(
        user_id=user.user_id,
        username=user.username,
        email=user.email,
        role_id=user.role_id,
        **access_token,
    )

    return public_response, login_response


async def refresh_access_token(session, token: str):
    refresh_token = decode_refresh_token(token)
    if not refresh_token:
        return None

    user_id = int(refresh_token.sub)
    user = await crud.get_user_by_id(session, user_id)
    if not user:
        return None

    user_data: dict[str, Any] = {
        'user_id': user.user_id,
        'username': user.username,
        'email': user.email,
        'role_id': user.role_id,
    }

    access_token = encode_access_token(user_data)
    return RefreshResponse(
        **access_token,
    )


# async def get_current_user(token: 'str', session: AsyncSession) -> UserOrm | None:
#     decoded_token: TokenData | None = decode_access_token(token=token)
#     if not decoded_token:
#         return None
#
#     user_id: str = decoded_token.sub
#     user = await crud.get_user_by_id(session, int(user_id))
#     if not user:
#         return None
#     return user
