from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class PermissionOrm(Base):
    __tablename__ = 'permissions'

    permission_id: Mapped[int] = mapped_column(primary_key=True)
    permission_code: Mapped[str]
    permission_description: Mapped[str]
