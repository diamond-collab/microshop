from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


if TYPE_CHECKING:
    from .orders import OrderOrm
    from .product import Product


class OrderProductAssoc(Base):
    __tablename__ = 'order_product_association'

    order_product_id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey('orders.order_id'))
    product_id: Mapped[int] = mapped_column(ForeignKey('products.product_id'))
    quantity: Mapped[int]
    unit_price: Mapped[int]

    order: Mapped['OrderOrm'] = relationship(back_populates='order_items')
    product: Mapped['Product'] = relationship(back_populates='order_items')
