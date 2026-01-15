from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from .jwt import decode_jwt_token
from microshop.core.models.db_helper import db_helper
from microshop.api_v1.user import crud
from microshop.core.models.user import UserOrm


oauth2_scheme = HTTPBearer()


async def current_user(
    session: AsyncSession = Depends(db_helper.get_session), payload=Depends(oauth2_scheme)
) -> UserOrm | None:
    raw_token = payload.credentials
    # Получаем данные из токена
    token_data = decode_jwt_token(token=raw_token)
    user_id = int(token_data.sub)  # Берем айди пользователя
    # Находим пользователя в БД по его id
    user = await crud.get_user_by_id(session=session, user_id=user_id)

    return user


def require_permission(permission_user: str):
    async def dep(user: UserOrm = Depends(current_user)) -> None:
        if user.role.role_name.lower() == 'admin':
            return

        if permission_user not in {perm.permission_code for perm in user.role.permissions}:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Permission denied',
            )

    return dep
