from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession


from microshop.core.models import Product


async def get_products(session: AsyncSession) -> list[Product]:
    stmt = select(Product).order_by(Product.product_id)
    result: Result = await session.execute(stmt)
    products = result.scalars().all()
    return list(products)


async def get_product_by_id(session: AsyncSession, product_id: int) -> Product | None:
    return await session.get(Product, product_id)
