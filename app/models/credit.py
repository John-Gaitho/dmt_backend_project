import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, Text, DateTime
from app.database import Base

class CreditRecord(Base):
    __tablename__ = "credit_records"

    id = Column(
        String,
        primary_key=True,
        index=True,
        default=lambda: str(uuid.uuid4())
    )

    customer_name = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    id_number = Column(String, nullable=True)
    product_name = Column(String, nullable=False)

    quantity = Column(Integer, default=1)

    amount = Column(Float, nullable=False)
    paid_amount = Column(Float, default=0)
    balance = Column(Float, default=0)

    sale_date = Column(String)
    due_date = Column(String, nullable=True)

    notes = Column(Text, nullable=True)

    status = Column(String, default="unpaid")

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )