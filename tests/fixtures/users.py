from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from microshop.api_v1.user.security import hash_password
from microshop.core.models import RoleOrm, UserOrm


async def get_or_create_role(db_session: AsyncSession, role_name: str) -> RoleOrm:
    stmt = select(RoleOrm).where(RoleOrm.role_name == role_name)
    role = await db_session.scalar(stmt)
    if role is None:
        role = RoleOrm(role_name=role_name)
        db_session.add(role)
        await db_session.flush()

    return role


async def create_user(
    db_session: AsyncSession,
    *,
    username: str,
    email: str,
    password: str,
    role_name: str,
) -> UserOrm:
    stmt = select(UserOrm).where(UserOrm.email == email)
    user = await db_session.scalar(stmt)

    if user is None:
        role = await get_or_create_role(db_session, role_name)

        user = UserOrm(
            username=username,
            email=email,
            hashed_password=hash_password(password),
            role_id=role.role_id,
            is_active=True,
        )

        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)

    return user
