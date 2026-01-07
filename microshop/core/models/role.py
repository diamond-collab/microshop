from typing import TYPE_CHECKING

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


if TYPE_CHECKING:
    from .user import UserOrm


class RoleOrm(Base):
    __tablename__ = 'roles'

    role_id: Mapped[int] = mapped_column(primary_key=True)
    role_name: Mapped[str] = mapped_column(String(25), unique=True)
    role_description: Mapped[str] = mapped_column(Text, nullable=True)

    # Список пользователей будет автоматически доступен через RelationMixin
    users: Mapped[list['UserOrm']] = relationship(back_populates='role')
