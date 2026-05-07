from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.models.base import Base   # 🔥 FIXED IMPORT


class Order(Base):
    __tablename__ = "orders"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, nullable=True)

    total_amount = Column(Float, nullable=False)
    status = Column(String, default="pending")

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 🔥 RELATIONSHIP (for Option 2 fix)
    items = relationship(
        "OrderItem",
        backref="order",
        cascade="all, delete-orphan"
    )