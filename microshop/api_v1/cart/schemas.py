from pydantic import BaseModel, Field


class CartItemAddRequest(BaseModel):
    product_id: int
    quantity: int


class CartItemResponse(BaseModel):
    cart_item_id: int
    product_id: int
    quantity: int
    unit_price: int
    line_total: int


class CartResponse(BaseModel):
    cart_id: int
    items: list[CartItemResponse] = Field(default_factory=list)
    total_price: int

