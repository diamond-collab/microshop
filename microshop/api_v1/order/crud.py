# Orders
# 	1.	POST /api/v1/orders/ — оформить заказ (checkout)
# 	2.	GET /api/v1/orders/ — мои заказы
# 	3.	GET /api/v1/orders/{order_id} — детали моего заказа
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import (
    OrderResponse,
    OrderItemResponse,
    OrderListResponse,
    OrderItemResponse1,
    OrderResponse1,
)
from microshop.core.models import OrderOrm, OrderProductAssoc
from microshop.api_v1.cart import crud


async def create_order_from_cart(session: AsyncSession, user_id: int) -> OrderResponse | None:
    cart = await crud.get_active_cart_with_items(session=session, user_id=user_id)
    if not cart.cart_items:
        return None

    order = OrderOrm(user_id=user_id)

    session.add(order)
    await session.flush()

    order_items: list[tuple[OrderProductAssoc, int]] = list()
    total_price = 0

    for cart_item in cart.cart_items:
        line_total = cart_item.unit_price * cart_item.quantity
        total_price += line_total

        assoc = OrderProductAssoc(
            order_id=order.order_id,
            product_id=cart_item.product_id,
            quantity=cart_item.quantity,
            unit_price=cart_item.unit_price,
        )
        session.add(assoc)

        order_items.append((assoc, line_total))
    await session.flush()

    items_response: list[OrderItemResponse] = list()
    for assoc, line_total in order_items:
        items_response.append(
            OrderItemResponse(
                order_product_id=assoc.order_product_id,
                product_id=assoc.product_id,
                quantity=assoc.quantity,
                unit_price=assoc.unit_price,
                line_total=line_total,
            )
        )

    for cart_item in cart.cart_items:
        await session.delete(cart_item)

    await session.commit()
    return OrderResponse(
        order_id=order.order_id,
        order_state=order.order_state,
        created_at=order.created_at,
        items=items_response,
        total_price=total_price,
    )


async def database_query(session: AsyncSession, user_id: int) -> OrderOrm | None:
    pass


async def get_orders(session: AsyncSession, user_id: int) -> list[OrderListResponse] | None:
    stmt = (
        select(OrderOrm)
        .where(
            OrderOrm.user_id == user_id,
        )
        .options(selectinload(OrderOrm.order_items).joinedload(OrderProductAssoc.product))
    )
    orders = await session.scalars(stmt)
    orders_list: list[OrderListResponse] = list()

    for order in orders:
        total_price = 0
        for item in order.order_items:
            total_price += item.unit_price * item.quantity

        orders_list.append(
            OrderListResponse(
                order_id=order.order_id,
                order_state=order.order_state,
                created_at=order.created_at,
                total_price=total_price,
            )
        )

    return orders_list


async def get_order_by_id(
    session: AsyncSession,
    order_id: int,
    user_id: int,
) -> OrderResponse1 | None:
    stmt = (
        select(OrderOrm)
        .where(
            OrderOrm.user_id == user_id,
            OrderOrm.order_id == order_id,
        )
        .options(selectinload(OrderOrm.order_items).joinedload(OrderProductAssoc.product))
    )
    order = await session.scalar(stmt)
    if not order:
        return None

    order_items: list[OrderItemResponse1] = list()
    total_price = 0

    for item in order.order_items:  # type: OrderProductAssoc
        line_total = item.unit_price * item.quantity
        total_price += line_total

        order_items.append(
            OrderItemResponse1(
                order_product_id=item.order_product_id,
                product_id=item.product_id,
                product_name=item.product.product_name,
                product_description=item.product.description,
                quantity=item.quantity,
                unit_price=item.unit_price,
                line_total=line_total,
            )
        )

    return OrderResponse1(
        order_id=order.order_id,  # type: ignore[arg-type]
        order_state=order.order_state,  # type: ignore[arg-type]
        created_at=order.created_at,  # type: ignore[arg-type]
        items=order_items,
        total_price=total_price,
    )
