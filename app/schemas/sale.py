from pydantic import BaseModel
from typing import Optional
from datetime import date


class SaleCreate(BaseModel):

    invoice_number: str

    product_id: Optional[str]

    product_name: str

    category: str

    quantity: int

    buying_price: float

    selling_price: float

    total_amount: float

    profit: float

    payment_method: str

    customer_name: Optional[str]

    notes: Optional[str]

    sale_date: date


class SaleResponse(SaleCreate):

    id: str

    class Config:
        from_attributes = True