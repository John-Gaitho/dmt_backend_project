from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_session
from app.models.product import Product

from app.schemas.product import (
    ProductCreate,
    ProductUpdate,
)

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

# =========================
# CREATE PRODUCT
# =========================

@router.post("/")
async def create_product(
    product: ProductCreate,
    session: AsyncSession = Depends(get_session)
):

    new_product = Product(
        name=product.name,
        price=product.price,
        category=product.category,
        description=product.description,
        stock_quantity=product.stock_quantity,
        image_urls=product.image_urls
    )

    session.add(new_product)

    await session.commit()
    await session.refresh(new_product)

    return new_product


# =========================
# GET PRODUCTS
# =========================

@router.get("/")
async def get_products(
    session: AsyncSession = Depends(get_session)
):

    result = await session.execute(
        select(Product)
    )

    return result.scalars().all()


# =========================
# UPDATE PRODUCT ⭐ FIXED
# =========================

@router.put("/{product_id}")
async def update_product(
    product_id: str,
    product: ProductUpdate,
    session: AsyncSession = Depends(get_session)
):

    result = await session.execute(
        select(Product).where(
            Product.id == product_id
        )
    )

    db_product = result.scalar_one_or_none()

    if not db_product:

        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    # Update fields dynamically

    for key, value in product.dict().items():

        setattr(
            db_product,
            key,
            value
        )

    await session.commit()
    await session.refresh(db_product)

    return db_product


# =========================
# DELETE PRODUCT
# =========================

@router.delete("/{product_id}")
async def delete_product(
    product_id: str,
    session: AsyncSession = Depends(get_session)
):

    result = await session.execute(
        select(Product).where(
            Product.id == product_id
        )
    )

    product = result.scalar_one_or_none()

    if product:

        await session.delete(product)
        await session.commit()

        return {
            "message": "Product deleted"
        }

    raise HTTPException(
        status_code=404,
        detail="Product not found"
    )