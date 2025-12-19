from typing import TYPE_CHECKING

from datetime import datetime

from sqlalchemy import String, text, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixin import RelationMixin

if TYPE_CHECKING:
    from .role import RoleOrm


class UserOrm(RelationMixin, Base):
    __tablename__ = 'users'

    user_id: Mapped[int] = mapped_column(primary_key=True)
    role_user_id: Mapped[int] = mapped_column()  # Поле для роли пользователя
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

    # Настраиваем Mixin для связи с Role
    _target_table = "roles"
    _target_column = "role_id"
    _back_populates = "users"
    _unique = False
    _nullable = False

    roles: Mapped['RoleOrm'] = relationship(back_populates=_back_populates)
