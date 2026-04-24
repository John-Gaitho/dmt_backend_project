from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from datetime import date

from app.database import get_session

from app.models.product import Product
from app.models.sale import Sale
from app.models.sale_item import SaleItem

from app.schemas.sale import (
    SaleCreate,
    SaleItemCreate
)

router = APIRouter(
    prefix="/sales",
    tags=["Sales"]
)


# =====================================================
# CREATE SALE
# =====================================================

@router.post("/")
async def create_sale(
    sale_data: SaleCreate,
    session: AsyncSession = Depends(get_session)
):
    total_amount = 0

    new_sale = Sale()

    session.add(new_sale)

    await session.flush()

    for item in sale_data.items:

        product_id = item.product_id
        quantity = item.quantity

        result = await session.execute(
            select(Product).where(
                Product.id == product_id
            )
        )

        product = result.scalar_one_or_none()

        if not product:
            raise HTTPException(
                status_code=404,
                detail=f"Product {product_id} not found"
            )

        if product.stock_quantity < quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Not enough stock for {product.name}"
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

    await session.refresh(new_sale)

    return {
        "message": "Sale created",
        "sale_id": new_sale.id,
        "total_amount": total_amount
    }


# =====================================================
# GET SALES (ALL or BY DATE)
# =====================================================

@router.get("/")
async def get_sales(
    sale_date: Optional[date] = Query(
        None,
        description="Filter sales by date"
    ),
    session: AsyncSession = Depends(get_session)
):
    query = select(Sale)

    if sale_date:
        query = query.where(
            Sale.created_at == sale_date
        )

    result = await session.execute(query)

    sales = result.scalars().all()

    return sales


# =====================================================
# DELETE SALE
# =====================================================

@router.delete("/{sale_id}")
async def delete_sale(
    sale_id: int,
    session: AsyncSession = Depends(get_session)
):
    result = await session.execute(
        select(Sale).where(
            Sale.id == sale_id
        )
    )

    sale = result.scalar_one_or_none()

    if not sale:
        raise HTTPException(
            status_code=404,
            detail="Sale not found"
        )

    await session.delete(sale)

    await session.commit()

    return {
        "message": "Sale deleted"
    }


# =====================================================
# SALES SUMMARY (BONUS — VERY USEFUL)
# =====================================================

@router.get("/summary")
async def sales_summary(
    sale_date: Optional[date] = None,
    session: AsyncSession = Depends(get_session)
):
    query = select(Sale)

    if sale_date:
        query = query.where(
            Sale.created_at == sale_date
        )

    result = await session.execute(query)

    sales = result.scalars().all()

    total_sales = len(sales)

    total_amount = sum(
        float(s.total_amount)
        for s in sales
        if s.total_amount
    )

    return {
        "total_sales": total_sales,
        "total_amount": total_amount
    }