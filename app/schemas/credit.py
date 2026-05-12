from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


# =========================================
# CREDIT ITEM — input (create/update)
# =========================================

class CreditItemBase(BaseModel):
    product_name: str
    quantity: int = 1
    amount: float
    paid_amount: float = 0
    sale_date: str
    due_date: Optional[str] = None
    notes: Optional[str] = None


# Used by the POST /{account_id}/items endpoint
CreditItemCreate = CreditItemBase


# =========================================
# CREDIT ITEM — response (read)
# =========================================

class CreditItemResponse(CreditItemBase):
    id: str
    account_id: str
    balance: float
    
    class Config:
        from_attributes = True


# =========================================
# CREDIT ACCOUNT — create
# =========================================

class CreditCreate(BaseModel):
    customer_name: str
    phone: Optional[str] = None
    id_number: Optional[str] = None
    items: List[CreditItemBase]


# =========================================
# CREDIT ACCOUNT — update
# =========================================

class CreditUpdate(CreditCreate):
    pass


# =========================================
# CREDIT ACCOUNT — response (read)
# =========================================

class CreditAccountResponse(BaseModel):
    id: str
    customer_name: str
    phone: Optional[str] = None
    id_number: Optional[str] = None
    total_amount: float
    total_paid: float
    balance: float
    status: str
    created_at: datetime
    items: List[CreditItemResponse]

    class Config:
        from_attributes = True