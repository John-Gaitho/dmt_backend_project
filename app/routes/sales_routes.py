from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from uuid import UUID

from app.database import get_db
from app.models.sale import Sale
from app.schemas.sale import SaleCreate, SaleResponse

router = APIRouter(
    prefix="/sales",
    tags=["Sales"]
)

# ======================================================
# CREATE SALE
# ======================================================
@router.post(
    "/",
    response_model=SaleResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_sale(
    sale: SaleCreate,
    db: AsyncSession = Depends(get_db)
):
    db_sale = Sale(**sale.dict())

    db.add(db_sale)
    await db.commit()
    await db.refresh(db_sale)

    return db_sale


# ======================================================
# GET ALL SALES
# ======================================================
@router.get(
    "/",
    response_model=list[SaleResponse]
)
async def get_sales(
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Sale))
    sales = result.scalars().all()

    return sales


# ======================================================
# GET SINGLE SALE
# ======================================================
@router.get(
    "/{sale_id}",
    response_model=SaleResponse
)
async def get_sale(
    sale_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Sale).where(Sale.id == str(sale_id))
    )

    sale = result.scalar_one_or_none()

    if not sale:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sale not found"
        )

    return sale


# ======================================================
# UPDATE SALE
# ======================================================
@router.put(
    "/{sale_id}",
    response_model=SaleResponse
)
async def update_sale(
    sale_id: UUID,
    updated_sale: SaleCreate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Sale).where(Sale.id == str(sale_id))
    )

    sale = result.scalar_one_or_none()

    if not sale:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sale not found"
        )

    for key, value in updated_sale.dict().items():
        setattr(sale, key, value)

    await db.commit()
    await db.refresh(sale)

    return sale


# ======================================================
# DELETE SALE
# ======================================================
@router.delete(
    "/{sale_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_sale(
    sale_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Sale).where(Sale.id == str(sale_id))
    )

    sale = result.scalar_one_or_none()

    if not sale:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sale not found"
        )

    await db.delete(sale)
    await db.commit()

    return None