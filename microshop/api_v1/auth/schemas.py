import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'Bearer'


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class RefreshRequest(BaseModel):
    refresh_token: str


class AccessTokenPayload(BaseModel):
    sub: str
    username: str
    email: EmailStr
    role_id: int | None
    exp: datetime.datetime


class RefreshTokenPayload(BaseModel):
    sub: str
    type_token: str
    exp: datetime.datetime
    jti: str


class TokenData(BaseModel):
    sub: str
    username: str | None = None
    email: EmailStr | None = None
    role_id: int | None = None
    type_token: Optional[str] = None


# class RefreshTokenData(BaseModel):
#     sub: str
#     type_token: str
#     exp: datetime.datetime


class LoginResponse(BaseModel):
    user_id: int
    username: str
    email: str
    role_id: int
    access_token: str
    refresh_token: str
    token_type: str = 'bearer'


class RefreshResponse(BaseModel):
    access_token: str
    token_type: str = 'bearer'


class ResponseUser(BaseModel):
    user_id: int
    username: str
    email: str
    role_id: int
