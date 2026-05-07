from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


# =========================
# ORDER ITEM
# =========================
class OrderItemBase(BaseModel):
    product_id: str
    product_name: str
    quantity: int
    price: float


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemResponse(OrderItemBase):
    pass


# =========================
# ORDER
# =========================
class OrderBase(BaseModel):
    user_id: Optional[str] = None
    total_amount: float
    status: Optional[str] = "pending"


class OrderCreate(OrderBase):
    items: List[OrderItemCreate]


class OrderUpdate(BaseModel):
    status: Optional[str] = None


class OrderResponse(OrderBase):
    id: str
    created_at: datetime
    items: List[OrderItemResponse] = []

    class Config:
        from_attributes = True
        