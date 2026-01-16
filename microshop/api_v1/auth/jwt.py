import uuid
from datetime import datetime, timezone, timedelta

from jose import JWTError, jwt

from .schemas import (
    TokenData,
    AccessTokenPayload,
    RefreshTokenPayload,
)
from microshop.core.config import settings
from ...core.models import UserOrm


def encode_access_token(user: UserOrm | dict) -> dict:
    expires = datetime.now(timezone.utc) + timedelta(minutes=15)
    payload_obj = AccessTokenPayload(
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


def encode_refresh_token(user: UserOrm | dict) -> dict:
    expires = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    payload_obj = RefreshTokenPayload(
        sub=str(user.get('user_id')),
        type_token='refresh',
        exp=expires,
        jti=str(uuid.uuid4()),
    )

    payload = dict(payload_obj)
    refresh_token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return {
        'refresh_token': refresh_token,
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


def decode_access_token(token: str) -> TokenData | None:
    token_data = decode_jwt_token(token)
    if not token_data:
        return None

    if token_data.type_token == 'refresh':
        return None

    return token_data


def decode_refresh_token(token: str) -> TokenData | None:
    token_data = decode_jwt_token(token)
    if not token_data:
        return None

    if token_data.type_token != 'refresh':
        return None

    return token_data
