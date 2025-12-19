from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio.session import AsyncSession


from .schemas import UserCreate, UpdateUser
from .security import hash_password
from microshop.core.models import UserOrm


DEFAULT_USER_ROLE_ID = 2


async def create_user(session: AsyncSession, user_in: UserCreate) -> UserOrm:
    user = UserOrm(
        role_id=DEFAULT_USER_ROLE_ID,
        username=user_in.username,
        email=str(user_in.email),
        hashed_password=hash_password(user_in.password),
        is_active=True,
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def get_user_by_email(session: AsyncSession, email: str) -> UserOrm | None:
    stmt = select(UserOrm).where(UserOrm.email == email)
    result: Result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def get_user_by_id(session: AsyncSession, user_id: int) -> UserOrm | None:
    return await session.get(UserOrm, user_id)


async def update_data_user(session: AsyncSession, user_id: int, data: UpdateUser) -> UserOrm | None:
    user: UserOrm | None = await session.get(UserOrm, user_id)
    if not user:
        return None

    updated_data = data.model_dump(exclude_unset=True)
    for key, value in updated_data.items():
        if key == 'password':
            setattr(user, 'hashed_password', hash_password(value))
        else:
            setattr(user, key, value)

    await session.commit()
    await session.refresh(user)
    return user


async def delete_user(session: AsyncSession, user_id: int) -> bool | None:
    user: UserOrm | None = await session.get(UserOrm, user_id)
    if not user:
        return None

    await session.delete(user)
    await session.commit()
    return True
