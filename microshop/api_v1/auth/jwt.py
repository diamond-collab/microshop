from datetime import datetime, timezone, timedelta

from jose import JWTError, jwt

from .schemas import TokenData, TokenPayload
from microshop.core.config import settings
from ...core.models import UserOrm


def encode_jwt_token(user: UserOrm | dict) -> dict:
    expires = datetime.now(timezone.utc) + timedelta(minutes=15)
    payload_obj = TokenPayload(
        sub=str(user.get('user_id')),
        username=user.get('username'),
        email=user.get('email'),
        role_id=user.get('role_id'),
        exp=expires,
    )

    payload = dict(payload_obj)
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return {
        'access_token': token,
        'token_type': 'bearer',
    }


def decode_jwt_token(token: str) -> TokenData | None:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        exp = payload.get('exp')
        if exp is None or datetime.fromtimestamp(exp, timezone.utc) <= datetime.now(timezone.utc):
            return None

        return TokenData(**payload)
    except JWTError:
        return None
