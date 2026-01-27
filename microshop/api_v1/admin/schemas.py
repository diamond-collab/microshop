from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict


class UpdateProduct(BaseModel):
    model_config = ConfigDict(extra='forbid')
    product_name: str | None = None
    description: str | None = None
    price: int | None = None


class ResponseAllOrder(BaseModel):
    order_id: int
    user_id: int
    order_state: str
    created_at: datetime


class OrderState(str, Enum):
    created = 'created'
    paid = 'paid'
    shipped = 'shipped'
    delivered = 'delivered'
    cancelled = 'cancelled'


class OrderStatusUpdate(BaseModel):
    order_state: OrderState
