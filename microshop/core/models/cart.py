from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, func, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


if TYPE_CHECKING:
    from .user import UserOrm


class CartOrm(Base):
    __tablename__ = 'cart'

    cart_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.user_id'),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        default=datetime.now,
    )
    is_active: Mapped[bool] = mapped_column(
        server_default=text('true'),
        default=False,
        nullable=False,
    )

    user: Mapped['UserOrm'] = relationship(back_populates='carts')
