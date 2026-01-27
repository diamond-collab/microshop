from sqlalchemy.ext.asyncio import AsyncSession

from microshop.core.models.user import UserOrm


async def delete_user(session: AsyncSession, user_id: int) -> bool | None:
    user: UserOrm | None = await session.get(UserOrm, user_id)
    if not user:
        return None

    await session.delete(user)
    await session.commit()
    return True
