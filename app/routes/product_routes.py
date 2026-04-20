from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_session
from app.models.product import Product

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


# Create Product
@router.post("/")
async def create_product(
    name: str,
    price: float,
    category: str = "",
    description: str = "",
    stock_quantity: int = 100,
    session: AsyncSession = Depends(get_session)
):
    new_product = Product(
        name=name,
        price=price,
        category=category,
        description=description,
        stock_quantity=stock_quantity
    )

    session.add(new_product)
    await session.commit()
    await session.refresh(new_product)

    return new_product


# Get All Products
@router.get("/")
async def get_products(
    session: AsyncSession = Depends(get_session)
):
    result = await session.execute(
        select(Product)
    )

    products = result.scalars().all()

    return products


# Delete Product
@router.delete("/{product_id}")
async def delete_product(
    product_id: str,
    session: AsyncSession = Depends(get_session)
):
    result = await session.execute(
        select(Product).where(Product.id == product_id)
    )

    product = result.scalar_one_or_none()

    if product:
        await session.delete(product)
        await session.commit()

        return {"message": "Product deleted"}

    return {"message": "Product not found"}