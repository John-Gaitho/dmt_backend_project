import uuid

from sqlalchemy import Column, String, Boolean, Numeric, Integer, Text

from app.models.base import Base


class Product(Base):
    __tablename__ = "products"

    # Use String instead of UUID for SQLite
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    name = Column(String, nullable=False)

    price = Column(Numeric, default=0)

    category = Column(String)

    description = Column(Text)

    in_stock = Column(Boolean, default=True)

    stock_quantity = Column(Integer, default=100)