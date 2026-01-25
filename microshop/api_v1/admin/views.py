from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status


from . import crud
from microshop.api_v1.auth.dependencies import require_permission
from microshop.api_v1.product.schemas import ProductCreate, Product
from microshop.core.models.db_helper import db_helper


# {
#   "email": "admin@email.ru",
#   "password": "admin123"
# }


router = APIRouter(tags=['Admin'])


@router.post(
    '/product',
    response_model=Product,
    dependencies=[Depends(require_permission('product:create'))],
)
async def create_product(
    product_in: ProductCreate, session: AsyncSession = Depends(db_helper.get_session)
):
    return await crud.create_product(session=session, product_in=product_in)


@router.delete(
    '/user/{user_id}/',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_permission('user:delete'))],
)
async def delete_data_user(user_id: int, session: AsyncSession = Depends(db_helper.get_session)):
    result = await crud.delete_user(session=session, user_id=user_id)
    if result is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f'User with id {user_id} not found')
