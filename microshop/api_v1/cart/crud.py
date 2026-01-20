# Минимальный набор эндпоинтов (MVP)
#
# Cart
# 	1.	GET /api/v1/cart/ — получить текущую корзину пользователя
# 	2.	POST /api/v1/cart/items/ — добавить товар или увеличить количество
# 	3.	PATCH /api/v1/cart/items/{item_id} — изменить количество
# 	4.	DELETE /api/v1/cart/items/{item_id} — удалить позицию
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import CartResponse, CartItemResponse, CartItemAddRequest
from microshop.core.models import CartOrm, CartItemAssocOrm
from microshop.api_v1.product import crud


async def get_or_create_cart(session: AsyncSession, user_id: int) -> CartOrm:
    stmt = select(CartOrm).where(CartOrm.user_id == user_id, CartOrm.is_active == True)
    cart = await session.scalar(stmt)

    if cart:
        return cart

    cart = CartOrm(
        user_id=user_id,
        is_active=True,
        # created_at=datetime.now(timezone.utc),
    )
    session.add(cart)
    await session.flush()
    return cart


async def get_cart(session: AsyncSession, user_id: int) -> CartResponse:
    cart = await get_or_create_cart(session=session, user_id=user_id)

    stmt = (
        select(CartOrm)
        .where(CartOrm.cart_id == cart.cart_id)
        .options(selectinload(CartOrm.cart_items).joinedload(CartItemAssocOrm.product))
    )
    cart_with_items = await session.scalar(stmt)

    total_price = 0
    items = []
    for item in cart_with_items.cart_items:  # type: CartItemAssocOrm
        line_total = item.unit_price * item.quantity
        total_price += line_total

        cart_item_response = CartItemResponse(
            cart_item_id=item.cart_item_id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=item.unit_price,
            line_total=line_total,
        )
        items.append(cart_item_response)

    cart_response = CartResponse(
        cart_id=cart_with_items.cart_id,  # type: ignore[arg-type]
        items=items,
        total_price=total_price,
    )

    return cart_response


async def add_item(
    session: AsyncSession,
    user_id: int,
    cart_item_add: CartItemAddRequest,
) -> CartResponse | None:
    if cart_item_add.quantity <= 0:
        return None

    product = await crud.get_product_by_id(session=session, product_id=cart_item_add.product_id)
    if not product:
        return None

    cart = await get_or_create_cart(session=session, user_id=user_id)
    stmt = select(CartItemAssocOrm).where(
        CartItemAssocOrm.cart_id == cart.cart_id,
        CartItemAssocOrm.product_id == product.product_id,
    )
    item_assoc = await session.scalar(stmt)
    if item_assoc:
        item_assoc.quantity += cart_item_add.quantity
        await session.commit()
        return await get_cart(session=session, user_id=user_id)

    added_item = CartItemAssocOrm(
        cart_id=cart.cart_id,
        product_id=product.product_id,
        quantity=cart_item_add.quantity,
        unit_price=product.price,
        # created_at=datetime.now(timezone.utc),
    )
    session.add(added_item)
    await session.commit()

    return await get_cart(session=session, user_id=user_id)
