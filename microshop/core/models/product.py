from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String, Float

from .base import Base


class Product(Base):
    product_id: Mapped[int] = mapped_column(primary_key=True)
    product_name: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String(255))
    price: Mapped[float] = mapped_column(Float)
