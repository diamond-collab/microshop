from sqlalchemy.ext.asyncio import AsyncSession

from microshop.core.models import UserOrm
from microshop.core.models.product import Product
from microshop.api_v1.product.schemas import ProductCreate


async def create_product(session: AsyncSession, product_in: ProductCreate) -> Product:
    product = Product(**product_in.model_dump())
    session.add(product)
    await session.commit()
    await session.refresh(product)
    return product


async def delete_user(session: AsyncSession, user_id: int) -> bool | None:
    user: UserOrm | None = await session.get(UserOrm, user_id)
    if not user:
        return None

    await session.delete(user)
    await session.commit()
    return True
