from sqlalchemy import Column, String, Integer, Float, ForeignKey
from app.models.base import Base


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(String, primary_key=True)
    order_id = Column(String, ForeignKey("orders.id"), nullable=False)

    product_id = Column(String, nullable=False)
    product_name = Column(String, nullable=False)

    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)