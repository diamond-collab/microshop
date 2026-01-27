from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from microshop.api_v1.admin.schemas import OrderState
from microshop.core.models import OrderOrm, OrderProductAssoc


async def get_orders(
    session: AsyncSession,
    state: str,
    limit: int,
    offset: int,
) -> list[OrderOrm]:
    stmt = (
        select(OrderOrm)
        .where(OrderOrm.order_state == state)
        .order_by(OrderOrm.created_at.desc())
        .limit(limit)
        .offset(offset)
    )
    result = await session.scalars(stmt)
    rows = list(result)
    if not rows:
        return []

    return rows


async def get_order_details(session: AsyncSession, order_id: int) -> OrderOrm | None:
    stmt = (
        select(OrderOrm)
        .where(OrderOrm.order_id == order_id)
        .options(selectinload(OrderOrm.order_items).joinedload(OrderProductAssoc.product))
    )

    result = await session.scalar(stmt)
    if not result:
        return None

    return result


async def update_order_status(
    session: AsyncSession,
    order_id: int,
    new_state: OrderState,
) -> OrderOrm | None:
    stmt = select(OrderOrm).where(OrderOrm.order_id == order_id)
    result = await session.scalar(stmt)

    if not result:
        return None

    result.order_state = new_state.value

    await session.commit()
    await session.refresh(result)

    return result
