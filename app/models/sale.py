import uuid
from datetime import datetime, date

from sqlalchemy import (
    Column,
    String,
    DateTime,
    Numeric,
    Integer,
    Date
)

from app.models.base import Base


class Sale(Base):
    __tablename__ = "sales"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    invoice_number = Column(
        String,
        unique=True,
        nullable=False
    )

    product_id = Column(
        String,
        nullable=True
    )

    product_name = Column(
        String,
        nullable=False
    )

    category = Column(
        String,
        nullable=True
    )

    quantity = Column(
        Integer,
        nullable=False
    )

    buying_price = Column(
        Numeric,
        nullable=False
    )

    selling_price = Column(
        Numeric,
        nullable=False
    )

    total_amount = Column(
        Numeric,
        nullable=False
    )

    profit = Column(
        Numeric,
        nullable=False
    )

    payment_method = Column(
        String,
        nullable=False
    )

    customer_name = Column(
        String,
        nullable=True
    )

    notes = Column(
        String,
        nullable=True
    )

    sale_date = Column(
        Date,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )