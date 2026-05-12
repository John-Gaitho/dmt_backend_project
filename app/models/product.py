import uuid
from sqlalchemy import Column, String, Float, Integer, Boolean, JSON, Text
from app.models.base import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)

    original_price = Column(Float, nullable=True)

    category = Column(String, default="")
    subcategory = Column(String, default="")

    stock_quantity = Column(Integer, default=0)
    in_stock = Column(Boolean, default=True)

    discount = Column(Integer, default=0)
    rating = Column(Float, default=0)

    featured = Column(Boolean, default=False)
    deal = Column(Boolean, default=False)

    description = Column(Text, default="")

    image_urls = Column(JSON, default=list)