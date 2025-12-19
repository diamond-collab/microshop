from pydantic import BaseModel, ConfigDict


class ProductBase(BaseModel):
    product_name: str
    description: str
    price: float


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    model_config = ConfigDict(from_attributes=True)
    product_id: int
