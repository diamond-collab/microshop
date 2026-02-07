from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import CartItemAddRequest, CartResponse
from .crud import add_item, get_cart
from microshop.core.models import UserOrm
from microshop.core.models.db_helper import db_helper
from microshop.api_v1.auth.dependencies import current_user


router = APIRouter(tags=['Cart'])


@router.post('/items/', response_model=CartResponse)
async def add_cart(
    cart_item_in: CartItemAddRequest,
    session: AsyncSession = Depends(db_helper.get_session),
    user: UserOrm = Depends(current_user),
) -> CartResponse:
    if cart_item_in.quantity <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Quantity must be greater than zero',
        )

    cart_items = await add_item(
        session=session,
        user_id=user.user_id,
        cart_item_add=cart_item_in,
    )
    if cart_items is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Product not found',
        )

    return cart_items


@router.get('/cart/', response_model=CartResponse)
async def get_my_cart(
    session: AsyncSession = Depends(db_helper.get_session),
    user: UserOrm = Depends(current_user),
) -> CartResponse:
    return await get_cart(
        session=session,
        user_id=user.user_id,
    )
