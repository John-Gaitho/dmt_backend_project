from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.product import Product

router = APIRouter(
    prefix="/order-items",
    tags=["Order Items"]
)

# =========================
# GET all order items
# =========================

@router.get("/")
async def get_order_items(
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(SaleItem)
    )
    items = result.scalars().all()
    return items


# =========================
# GET order items by order
# =========================

@router.get("/order/{order_id}")
async def get_items_by_order(
    order_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(SaleItem)
        .where(SaleItem.sale_id == order_id)
    )

    items = result.scalars().all()
    return items


# =========================
# CREATE order item
# =========================

@router.post("/")
async def create_order_item(
    sale_id: int,
    product_id: int,
    quantity: int,
    price: float,
    db: AsyncSession = Depends(get_db)
):
    # Check product exists
    result = await db.execute(
        select(Product)
        .where(Product.id == product_id)
    )

    product = result.scalar_one_or_none()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    # Create order item
    new_item = SaleItem(
        sale_id=sale_id,
        product_id=product_id,
        quantity=quantity,
        price=price
    )

    db.add(new_item)
    await db.commit()
    await db.refresh(new_item)

    return new_item


# =========================
# UPDATE order item
# =========================

@router.put("/{item_id}")
async def update_order_item(
    item_id: int,
    quantity: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(SaleItem)
        .where(SaleItem.id == item_id)
    )

    item = result.scalar_one_or_none()

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Order item not found"
        )

    item.quantity = quantity

    await db.commit()
    await db.refresh(item)

    return item


# =========================
# DELETE order item
# =========================

@router.delete("/{item_id}")
async def delete_order_item(
    item_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(SaleItem)
        .where(SaleItem.id == item_id)
    )

    item = result.scalar_one_or_none()

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Order item not found"
        )

    await db.delete(item)
    await db.commit()

    return {
        "message": "Order item deleted successfully"
    }