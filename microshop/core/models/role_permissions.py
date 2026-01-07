from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class RolePermissionsAssoc(Base):
    __tablename__ = 'role_permissions'
    __table_args__ = (
        UniqueConstraint('role_id', 'permission_id', name='idx_unique_role_permission'),
    )

    role_permission_id: Mapped[int] = mapped_column(primary_key=True)
    role_id: Mapped[int] = mapped_column(ForeignKey('roles.role_id'))
    permission_id: Mapped[int] = mapped_column(ForeignKey('permissions.permission_id'))
