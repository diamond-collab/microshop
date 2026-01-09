from typing import TYPE_CHECKING

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String

from .base import Base


if TYPE_CHECKING:
    from .cart_items import CartItemAssocOrm


class Product(Base):
    product_id: Mapped[int] = mapped_column(primary_key=True)
    product_name: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String(255))
    price: Mapped[int]

    products_details: Mapped[list['CartItemAssocOrm']] = relationship(back_populates='product')
