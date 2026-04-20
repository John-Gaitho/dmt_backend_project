
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_session
from app.models.product import Product

router = APIRouter()

@router.get("/")
async def get_products(
        db: AsyncSession = Depends(get_session)):

    result = await db.execute(
        select(Product)
    )

    return result.scalars().all()


@router.post("/")
async def create_product(
        data: dict,
        db: AsyncSession = Depends(get_session)):

    product = Product(**data)

    db.add(product)

    await db.commit()

    return product
