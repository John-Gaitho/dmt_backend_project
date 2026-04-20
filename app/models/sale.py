import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, Numeric
from sqlalchemy.orm import relationship

from app.models.base import Base


class Sale(Base):
    __tablename__ = "sales"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    total_amount = Column(
        Numeric,
        default=0
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    items = relationship(
        "SaleItem",
        back_populates="sale"
    )