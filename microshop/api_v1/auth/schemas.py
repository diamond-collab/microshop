import datetime

from pydantic import BaseModel, EmailStr


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenPayload(BaseModel):
    sub: str
    username: str
    email: EmailStr
    role_id: int | None
    exp: datetime.datetime


class TokenData(BaseModel):
    sub: str
    username: str
    email: EmailStr
    role_id: int | None


class LoginResponse(BaseModel):
    user_id: int
    username: str
    email: str
    role_id: int
    access_token: str
    token_type: str
