from sqlalchemy import Column, String, Integer, Float, ForeignKey
from app.models.base import Base


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(String, primary_key=True, index=True)
    order_id = Column(String, ForeignKey("orders.id"))
    product_id = Column(String, ForeignKey("products.id"))

    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)