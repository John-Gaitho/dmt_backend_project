import uuid

from datetime import datetime

from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    Text,
    DateTime,
    ForeignKey,
)

from sqlalchemy.orm import relationship

from app.database import Base


# =========================================
# CREDIT ACCOUNT (CUSTOMER)
# =========================================

class CreditAccount(Base):

    __tablename__ = "credit_accounts"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    customer_name = Column(
        String,
        nullable=False
    )

    phone = Column(
        String,
        nullable=True
    )

    id_number = Column(
        String,
        nullable=True
    )

    total_amount = Column(
        Float,
        default=0
    )

    total_paid = Column(
        Float,
        default=0
    )

    balance = Column(
        Float,
        default=0
    )

    status = Column(
        String,
        default="unpaid"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    # RELATIONSHIP

    items = relationship(
        "CreditItem",
        back_populates="account",
        cascade="all, delete"
    )


# =========================================
# CREDIT ITEMS (PRODUCTS)
# =========================================

class CreditItem(Base):

    __tablename__ = "credit_items"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    account_id = Column(
        String,
        ForeignKey("credit_accounts.id"),
        nullable=False
    )

    product_name = Column(
        String,
        nullable=False
    )

    quantity = Column(
        Integer,
        default=1
    )

    amount = Column(
        Float,
        nullable=False
    )

    paid_amount = Column(
        Float,
        default=0
    )

    balance = Column(
        Float,
        default=0
    )

    sale_date = Column(
        String
    )

    due_date = Column(
        String,
        nullable=True
    )

    notes = Column(
        Text,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    # RELATIONSHIP

    account = relationship(
        "CreditAccount",
        back_populates="items"
    )