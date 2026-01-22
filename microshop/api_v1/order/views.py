from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from microshop.core.models.db_helper import db_helper
from microshop.api_v1.auth.dependencies import current_user

from .crud import create_order_from_cart, get_orders, get_order_by_id
from .schemas import OrderResponse, OrderListResponse, OrderResponse1
from microshop.core.models.user import UserOrm

router = APIRouter(tags=['Order'])


@router.post('/', response_model=OrderResponse)
async def create_order(
    session: AsyncSession = Depends(db_helper.get_session),
    user: UserOrm = Depends(current_user),
) -> OrderResponse:
    order = await create_order_from_cart(session=session, user_id=user.user_id)
    if order is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Cart is empty',
        )

    return order


@router.get('/', response_model=list[OrderListResponse])
async def get_all_orders(
    session: AsyncSession = Depends(db_helper.get_session),
    user: UserOrm = Depends(current_user),
) -> list[OrderListResponse] | None:
    orders = await get_orders(session=session, user_id=user.user_id)
    if orders is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='You have no orders yet',
        )

    return orders


@router.get('/{order_id}', response_model=OrderResponse1)
async def get_current_order(
    order_id: int,
    session: AsyncSession = Depends(db_helper.get_session),
    user: UserOrm = Depends(current_user),
) -> OrderResponse1 | None:
    order = await get_order_by_id(session=session, order_id=order_id, user_id=user.user_id)
    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Order not found',
        )

    return order
