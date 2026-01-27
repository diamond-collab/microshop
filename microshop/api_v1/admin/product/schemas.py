from pydantic import BaseModel, ConfigDict, EmailStr


class UpdateProduct(BaseModel):
    model_config = ConfigDict(extra='forbid')
    product_name: str | None = None
    description: str | None = None
    price: int | None = None