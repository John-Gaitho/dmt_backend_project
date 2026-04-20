import uuid

from sqlalchemy import Column, String, Integer, Numeric, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import Base


class SaleItem(Base):
    __tablename__ = "sale_items"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    sale_id = Column(
        String,
        ForeignKey("sales.id")
    )

    product_id = Column(
        String,
        ForeignKey("products.id")
    )

    quantity = Column(
        Integer,
        nullable=False
    )

    price = Column(
        Numeric,
        nullable=False
    )

    sale = relationship(
        "Sale",
        back_populates="items"
    )