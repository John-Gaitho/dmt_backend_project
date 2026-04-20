from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_session

from app.models.product import Product
from app.models.sale import Sale
from app.models.sale_item import SaleItem

router = APIRouter(
    prefix="/sales",
    tags=["Sales"]
)


@router.post("/")
async def create_sale(
    items: list[dict],
    session: AsyncSession = Depends(get_session)
):
    total_amount = 0

    new_sale = Sale()

    session.add(new_sale)

    await session.flush()

    for item in items:

        product_id = item["product_id"]
        quantity = item["quantity"]

        result = await session.execute(
            select(Product).where(
                Product.id == product_id
            )
        )

        product = result.scalar_one_or_none()

        if not product:
            raise HTTPException(
                status_code=404,
                detail="Product not found"
            )

        if product.stock_quantity < quantity:
            raise HTTPException(
                status_code=400,
                detail="Not enough stock"
            )

        # Reduce stock
        product.stock_quantity -= quantity

        price = float(product.price)

        sale_item = SaleItem(
            sale_id=new_sale.id,
            product_id=product_id,
            quantity=quantity,
            price=price
        )

        session.add(sale_item)

        total_amount += price * quantity

    new_sale.total_amount = total_amount

    await session.commit()

    return {
        "message": "Sale created",
        "total": total_amount
    }