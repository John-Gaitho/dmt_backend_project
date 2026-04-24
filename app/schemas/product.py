from pydantic import BaseModel
from typing import Optional, List


class ProductBase(BaseModel):
    name: str
    price: float
    category: Optional[str] = ""
    description: Optional[str] = ""
    stock_quantity: Optional[int] = 100
    image_url: Optional[str] = None  # ✅ FIX


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    pass