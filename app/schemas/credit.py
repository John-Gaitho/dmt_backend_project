from pydantic import BaseModel
from typing import Optional


class CreditCreate(BaseModel):
    customer_name: str
    phone: Optional[str] = None
    id_number: Optional[str] = None
    product_name: str
    quantity: int = 1
    amount: float
    paid_amount: float
    sale_date: str
    due_date: Optional[str] = None
    notes: Optional[str] = None


class CreditUpdate(BaseModel):
    customer_name: Optional[str] = None
    phone: Optional[str] = None
    id_number: Optional[str] = None
    product_name: Optional[str] = None
    quantity: Optional[int] = None
    amount: Optional[float] = None
    paid_amount: Optional[float] = None
    sale_date: Optional[str] = None
    due_date: Optional[str] = None
    notes: Optional[str] = None