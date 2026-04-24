from pydantic import BaseModel
from typing import Optional


class OrderCreate(BaseModel):
    customer_name: Optional[str] = None
    total_amount: float
    payment_method: Optional[str] = None


class OrderUpdate(BaseModel):
    status: str