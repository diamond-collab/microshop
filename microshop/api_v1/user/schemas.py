from pydantic import BaseModel, ConfigDict, EmailStr, field_validator


class UserBase(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserCreate(UserBase):
    repeat_password: str

    @field_validator('repeat_password')
    def password_match(cls, v, info):
        password = info.data.get('password')
        if password != v:
            raise ValueError('Passwords do not match')
        return v


class UpdateUser(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None

    model_config = ConfigDict(from_attributes=True)


class UserResponse(BaseModel):
    user_id: int
    username: str
    email: EmailStr
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


# class User(UserBase):
#     model_config = ConfigDict(from_attributes=True)
#     user_id: int
#     username: str
#     email: EmailStr
