from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


if TYPE_CHECKING:
    from .product import Product
    from .cart import CartOrm


class CartItemAssocOrm(Base):
    __tablename__ = 'cart_item_assoc'

    cart_item_id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey('products.product_id'))
    cart_id: Mapped[int] = mapped_column(ForeignKey('cart.cart_id'))
    quantity: Mapped[int] = mapped_column(
        server_default='1',
        default=1,
        nullable=False,
    )
    unit_price: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        default=datetime.now,
        nullable=False,
    )

    product: Mapped['Product'] = relationship(back_populates='products_details')
    cart: Mapped['CartOrm'] = relationship(back_populates='cart_items')