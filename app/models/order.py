from sqlalchemy import Column, String, Float, DateTime
from sqlalchemy.sql import func
from app.models.base import Base


class Order(Base):
    __tablename__ = "orders"   # MUST be EXACT "orders"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, nullable=True)

    total_amount = Column(Float, nullable=False)
    status = Column(String, default="pending")

    created_at = Column(DateTime(timezone=True), server_default=func.now())