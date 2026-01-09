from typing import TYPE_CHECKING

from datetime import datetime

from sqlalchemy import String, text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .role import RoleOrm
    from .cart import CartOrm


class UserOrm(Base):
    __tablename__ = 'users'

    user_id: Mapped[int] = mapped_column(primary_key=True)
    role_id: Mapped[int] = mapped_column(
        ForeignKey('roles.role_id'),
        nullable=False,
    )
    username: Mapped[str] = mapped_column(
        String(25),
        nullable=False,
    )
    email: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True,
    )
    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(
        default=False,
        nullable=False,
        server_default=text('false'),
    )
    last_login: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    role: Mapped['RoleOrm'] = relationship(back_populates='users')
    carts: Mapped[list['CartOrm']] = relationship(back_populates='user')
