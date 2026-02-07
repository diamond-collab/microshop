from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from microshop.core.models import Product


async def create_product(
    db_session: AsyncSession,
    products: dict[str, dict[str, Any]],
) -> list[Product]:
    product_list = list()
    for item in products.values():
        product = Product(
            product_name=item['product_name'],
            description=item['description'],
            price=item['price'],
        )
        product_list.append(product)

    db_session.add_all(product_list)
    await db_session.flush()

    return product_list
