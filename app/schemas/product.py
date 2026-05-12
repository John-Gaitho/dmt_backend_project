from pydantic import BaseModel
from typing import Optional, List


# =========================
# BASE PRODUCT
# =========================

class ProductBase(BaseModel):
    name: str
    price: float
    category: Optional[str] = ""
    description: Optional[str] = ""
    stock_quantity: Optional[int] = 0
    image_urls: Optional[List[str]] = []


# =========================
# CREATE PRODUCT
# =========================

class ProductCreate(ProductBase):
    pass


# =========================
# UPDATE PRODUCT
# =========================

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    description: Optional[str] = None
    stock_quantity: Optional[int] = None
    image_urls: Optional[List[str]] = None