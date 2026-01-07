from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


if TYPE_CHECKING:
    from .role import RoleOrm


class PermissionOrm(Base):
    __tablename__ = 'permissions'

    permission_id: Mapped[int] = mapped_column(primary_key=True)
    permission_code: Mapped[str]
    permission_description: Mapped[str]

    # roles: Mapped[list['RoleOrm']] = relationship(
    #     secondary='role_permissions',
    #     back_populates='permissions',
    # )
