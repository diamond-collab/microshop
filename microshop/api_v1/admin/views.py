from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status


from . import crud
from microshop.api_v1.auth.dependencies import require_permission
from microshop.api_v1.product.schemas import ProductCreate, Product
from microshop.core.models.db_helper import db_helper
from microshop.core.models.orders import OrderOrm
from .schemas import UpdateProduct, ResponseAllOrder, OrderState, OrderStatusUpdate

# {
#   "email": "admin@email.ru",
#   "password": "admin123"
# }


router = APIRouter(tags=['Admin'])


@router.post(
    '/product/',
    response_model=Product,
    dependencies=[Depends(require_permission('product:create'))],
)
async def create_product(
    product_in: ProductCreate, session: AsyncSession = Depends(db_helper.get_session)
):
    return await crud.create_product(session=session, product_in=product_in)


@router.patch(
    '/product/{product_id}',
    dependencies=[Depends(require_permission('product:update'))],
)
async def update_product(
    product_id: int,
    product_in: UpdateProduct,
    session: AsyncSession = Depends(db_helper.get_session),
) -> Product:
    data = product_in.model_dump(exclude_unset=True)

    if not data:
        raise HTTPException(status_code=400, detail='No fields to update')

    product = await crud.product_update(
        session=session,
        product_id=product_id,
        product_in=product_in,
    )

    if product is None:
        raise HTTPException(status_code=404, detail=f'Product with id {product_id} not found')

    return product


###############
###-Order-###
###############
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


@router.patch(
    '/order/{order_id}/status',
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


@router.delete(
    '/user/{user_id}/',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_permission('user:delete'))],
)
async def delete_data_user(user_id: int, session: AsyncSession = Depends(db_helper.get_session)):
    result = await crud.delete_user(session=session, user_id=user_id)
    if result is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f'User with id {user_id} not found')
