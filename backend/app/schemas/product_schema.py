from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal
from typing import Optional


# Base model
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: Optional[Decimal] = Field(gt=0, decimal_places=2)
    stock_quantity: int = Field(ge=0, default=0)
    is_active: bool = True


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
