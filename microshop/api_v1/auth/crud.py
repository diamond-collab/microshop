from typing import Any

from sqlalchemy.ext.asyncio.session import AsyncSession

from .jwt import encode_jwt_token
from .schemas import UserLogin, LoginResponse
from microshop.api_v1.user import crud, security


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
