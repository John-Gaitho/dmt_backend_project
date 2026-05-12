from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_session
from app.models.credit import CreditRecord
from app.schemas.credit import CreditCreate, CreditUpdate

router = APIRouter()

# =========================
# GET ALL
# =========================
@router.get("/")
async def get_credits(session: AsyncSession = Depends(get_session)):
    result = await session.execute(
        select(CreditRecord).order_by(CreditRecord.created_at.desc())
    )
    return result.scalars().all()


# =========================
# CREATE
# =========================
@router.post("/")
async def create_credit(
    data: CreditCreate,
    session: AsyncSession = Depends(get_session)
):
    balance = data.amount - data.paid_amount

    if balance <= 0:
        status = "paid"
    elif data.paid_amount > 0:
        status = "partial"
    else:
        status = "unpaid"

    credit = CreditRecord(
        customer_name=data.customer_name,
        phone=data.phone,
        id_number=data.id_number,
        product_name=data.product_name,
        quantity=data.quantity,
        amount=data.amount,
        paid_amount=data.paid_amount,
        balance=balance,
        sale_date=data.sale_date,
        due_date=data.due_date,
        notes=data.notes,
        status=status,
    )

    session.add(credit)
    await session.commit()
    await session.refresh(credit)

    return credit


# =========================
# UPDATE
# =========================
@router.put("/{credit_id}")
async def update_credit(
    credit_id: str,   # ✅ FIXED (was int)
    data: CreditUpdate,
    session: AsyncSession = Depends(get_session)
):
    result = await session.execute(
        select(CreditRecord).where(CreditRecord.id == credit_id)
    )

    credit = result.scalar_one_or_none()

    if not credit:
        raise HTTPException(status_code=404, detail="Not found")

    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(credit, key, value)

    credit.balance = float(credit.amount) - float(credit.paid_amount)

    if credit.balance <= 0:
        credit.status = "paid"
    elif credit.paid_amount > 0:
        credit.status = "partial"
    else:
        credit.status = "unpaid"

    await session.commit()
    await session.refresh(credit)

    return credit


# =========================
# DELETE
# =========================
@router.delete("/{credit_id}")
async def delete_credit(
    credit_id: str,   # ✅ FIXED (was int)
    session: AsyncSession = Depends(get_session)
):
    result = await session.execute(
        select(CreditRecord).where(CreditRecord.id == credit_id)
    )

    credit = result.scalar_one_or_none()

    if not credit:
        raise HTTPException(status_code=404, detail="Not found")

    await session.delete(credit)
    await session.commit()

    return {"message": "Deleted"}