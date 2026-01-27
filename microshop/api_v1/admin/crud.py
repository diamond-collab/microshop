from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import OrderState
from microshop.api_v1.admin.schemas import UpdateProduct
from microshop.core.models import UserOrm
from microshop.core.models.product import Product
from microshop.core.models.orders import OrderOrm
from microshop.api_v1.product.schemas import ProductCreate
from microshop.api_v1.product import crud


###############
###-Product-###
###############
async def create_product(session: AsyncSession, product_in: ProductCreate) -> Product:
    product = Product(**product_in.model_dump())
    session.add(product)
    await session.commit()
    await session.refresh(product)
    return product


async def product_update(
    session: AsyncSession,
    product_in: UpdateProduct,
    product_id: int,
) -> Product | None:
    product = await crud.get_product_by_id(session=session, product_id=product_id)

    if not product:
        return None

    data = product_in.model_dump(exclude_unset=True, exclude_none=True)
    for field, value in data.items():
        setattr(product, field, value)

    await session.commit()
    await session.refresh(product)

    return product


###############
###-Order-###
###############
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


###############
###-User-###
###############
async def delete_user(session: AsyncSession, user_id: int) -> bool | None:
    user: UserOrm | None = await session.get(UserOrm, user_id)
    if not user:
        return None

    await session.delete(user)
    await session.commit()
    return True
