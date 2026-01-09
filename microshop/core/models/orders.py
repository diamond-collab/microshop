from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


if TYPE_CHECKING:
    from .order_items import OrderProductAssoc


class OrderOrm(Base):
    __tablename__ = 'orders'

    order_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id'))
    order_state: Mapped[str | None]
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        default=datetime.now,
        nullable=False,
    )

    order_items: Mapped[list['OrderProductAssoc']] = relationship(back_populates='order')
