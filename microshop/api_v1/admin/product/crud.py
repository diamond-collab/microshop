from sqlalchemy.ext.asyncio import AsyncSession

from microshop.api_v1.admin.product.schemas import UpdateProduct
from microshop.api_v1.product import crud
from microshop.api_v1.product.schemas import ProductCreate
from microshop.core.models import Product


async def create_product(session: AsyncSession, product_in: ProductCreate) -> Product:
    product = Product(**product_in.model_dump())
    session.add(product)
    await session.commit()
    await session.refresh(product)
    return product


async def product_update(
    session: AsyncSession,
    product_in: UpdateProduct,
    product_id: int,
) -> Product | None:
    product = await crud.get_product_by_id(session=session, product_id=product_id)

    if not product:
        return None

    data = product_in.model_dump(exclude_unset=True, exclude_none=True)
    for field, value in data.items():
        setattr(product, field, value)

    await session.commit()
    await session.refresh(product)

    return product
