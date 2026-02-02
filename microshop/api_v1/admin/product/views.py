from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession


from . import crud
from microshop.api_v1.admin.product.schemas import UpdateProduct
from microshop.api_v1.auth.dependencies import require_permission
from microshop.api_v1.product.schemas import Product, ProductCreate
from microshop.core.models.db_helper import db_helper


router = APIRouter(tags=['Admin • Product'])


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
