from datetime import datetime

from pydantic import BaseModel, Field


class OrderItemResponse(BaseModel):
    order_product_id: int
    product_id: int
    quantity: int
    unit_price: int
    line_total: int


class OrderResponse(BaseModel):
    order_id: int
    order_state: str
    created_at: datetime
    items: list[OrderItemResponse] = Field(default_factory=list)
    total_price: int


class OrderListResponse(BaseModel):
    order_id: int
    order_state: str
    created_at: datetime
    total_price: int


class OrderItemResponse1(BaseModel):
    order_product_id: int
    product_id: int
    product_name: str
    product_description: str
    quantity: int
    unit_price: int
    line_total: int


class OrderResponse1(BaseModel):
    order_id: int
    order_state: str | None
    created_at: datetime
    items: list[OrderItemResponse1] = Field(default_factory=list)
    total_price: int
