from typing import List

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from .schemas import Product, ProductCreate
from microshop.core.models.db_helper import db_helper

router = APIRouter(tags=['Products'])


@router.post('/', response_model=Product)
async def create_product(
    product_in: ProductCreate, session: AsyncSession = Depends(db_helper.get_session)
):
    return await crud.create_product(session=session, product_in=product_in)


@router.get('/', response_model=List[Product])
async def get_product(session: AsyncSession = Depends(db_helper.get_session)):
    return await crud.get_products(session=session)


@router.get('/{product_id}/', response_model=Product)
async def get_product_by_id(
    product_id: int, session: AsyncSession = Depends(db_helper.get_session)
):
    product = await crud.get_product_by_id(session=session, product_id=product_id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Product {product_id} not found!',
        )

    return product
