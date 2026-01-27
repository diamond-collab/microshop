from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from . import crud
from microshop.api_v1.auth.dependencies import require_permission
from microshop.api_v1.user.crud import get_user_by_id
from microshop.core.models.db_helper import db_helper
from microshop.api_v1.admin.schemas import (
    OrderState,
    ResponseAllOrder,
    OrderDetailResponse,
    OrderDetailItemsResponse,
    OrderStatusUpdate,
)


router = APIRouter(tags=['Admin • Order'])


@router.get(
    '/orders/',
    dependencies=[Depends(require_permission('order:read_all'))],
)
async def get_all_user_orders(
    state: OrderState = OrderState.created,
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    session: AsyncSession = Depends(db_helper.get_session),
) -> list[ResponseAllOrder]:
    result = await crud.get_orders(
        session=session,
        state=state.value,
        offset=offset,
        limit=limit,
    )

    orders: list[ResponseAllOrder] = list()
    for order in result:
        orders.append(
            ResponseAllOrder(
                order_id=order.order_id,
                user_id=order.user_id,
                order_state=order.order_state,
                created_at=order.created_at,
            )
        )

    return orders


@router.get(
    '/orders/{order_id}',
    response_model=OrderDetailResponse,
    dependencies=[Depends(require_permission('order:read'))],
)
async def get_detail_order(
    order_id: int,
    session: AsyncSession = Depends(db_helper.get_session),
):
    order = await crud.get_order_details(
        session=session,
        order_id=order_id,
    )
    if not order:
        raise HTTPException(
            status_code=404,
            detail=f'Order with id {order_id} not found',
        )

    user = await get_user_by_id(session=session, user_id=order.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with id {order_id} not found',
        )

    total_price = 0
    order_detail_items_response: list[OrderDetailItemsResponse] = list()
    for item in order.order_items:
        line_total = item.unit_price * item.quantity
        total_price += line_total

        order_detail_items_response.append(
            OrderDetailItemsResponse(
                product_id=item.product_id,
                product_name=item.product.product_name,
                description=item.product.description,
                price=item.product.price,
                unit_price=item.unit_price,
                quantity=item.quantity,
                line_total=line_total,
            )
        )

    return OrderDetailResponse(
        order_id=order.order_id,
        user_id=order.user_id,
        email=user.email,
        order_state=order.order_state,
        items=order_detail_items_response,
        total_price=total_price,
        created_at=order.created_at,
    )


@router.patch(
    '/orders/{order_id}/status',
    dependencies=[Depends(require_permission('order:status:update'))],
    response_model=ResponseAllOrder,
)
async def update_order_state(
    order_id: int,
    new_state: OrderStatusUpdate,
    session: AsyncSession = Depends(db_helper.get_session),
) -> ResponseAllOrder | None:
    result = await crud.update_order_status(
        session=session,
        order_id=order_id,
        new_state=new_state.order_state,
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail=f'Order with id {order_id} not found',
        )

    order = ResponseAllOrder(
        order_id=result.order_id,
        user_id=result.user_id,
        order_state=result.order_state,
        created_at=result.created_at,
    )

    return order
