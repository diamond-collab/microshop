from datetime import datetime

from pydantic import BaseModel
from enum import Enum

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


class OrderDetailItemsResponse(BaseModel):
    product_id: int
    product_name: str
    description: str | None
    price: int
    unit_price: int
    quantity: int
    line_total: int



class OrderDetailResponse(BaseModel):
    order_id: int
    user_id: int
    email: str
    order_state: str
    items: list[OrderDetailItemsResponse]
    total_price: int
    created_at: datetime