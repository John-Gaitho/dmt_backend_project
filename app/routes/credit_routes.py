from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List

import uuid

from app.database import get_session
from app.models.credit import (
    CreditAccount,
    CreditItem,
)
from app.schemas.credit import (
    CreditCreate,
    CreditUpdate,
    CreditAccountResponse,
    CreditItemCreate,
)

router = APIRouter()


# =========================================
# HELPERS
# =========================================

def compute_status(total_amount: float, total_paid: float) -> str:
    balance = total_amount - total_paid
    if balance <= 0:
        return "paid"
    if total_paid > 0:
        return "partial"
    return "unpaid"


# =========================================
# GET ALL CREDIT ACCOUNTS
# =========================================

@router.get("/", response_model=List[CreditAccountResponse])
async def get_credits(
    session: AsyncSession = Depends(get_session),
):
    result = await session.execute(
        select(CreditAccount)
        .options(selectinload(CreditAccount.items))
        .order_by(CreditAccount.created_at.desc())
    )
    return result.scalars().unique().all()


# =========================================
# GET SINGLE CREDIT ACCOUNT
# =========================================

@router.get("/{account_id}", response_model=CreditAccountResponse)
async def get_credit_account(
    account_id: str,
    session: AsyncSession = Depends(get_session),
):
    result = await session.execute(
        select(CreditAccount)
        .options(selectinload(CreditAccount.items))
        .where(CreditAccount.id == account_id)
    )
    account = result.scalar_one_or_none()
    if not account:
        raise HTTPException(status_code=404, detail="Customer not found")
    return account


# =========================================
# CREATE CREDIT ACCOUNT
# =========================================

@router.post("/", response_model=CreditAccountResponse)
async def create_credit(
    data: CreditCreate,
    session: AsyncSession = Depends(get_session),
):
    account_id = str(uuid.uuid4())

    account = CreditAccount(
        id=account_id,
        customer_name=data.customer_name,
        phone=data.phone,
        id_number=data.id_number,
    )

    total_amount = 0.0
    total_paid = 0.0

    for item in data.items:
        balance = item.amount - item.paid_amount
        credit_item = CreditItem(
            id=str(uuid.uuid4()),
            account_id=account_id,
            product_name=item.product_name,
            quantity=item.quantity,
            amount=item.amount,
            paid_amount=item.paid_amount,
            balance=balance,
            sale_date=item.sale_date,
            due_date=item.due_date,
            notes=item.notes,
        )
        session.add(credit_item)
        total_amount += item.amount
        total_paid += item.paid_amount

    account.total_amount = total_amount
    account.total_paid = total_paid
    account.balance = total_amount - total_paid
    account.status = compute_status(total_amount, total_paid)

    session.add(account)
    await session.commit()

    result = await session.execute(
        select(CreditAccount)
        .options(selectinload(CreditAccount.items))
        .where(CreditAccount.id == account_id)
    )
    return result.scalar_one()


# =========================================
# UPDATE CREDIT ACCOUNT
# =========================================

@router.put("/{account_id}", response_model=CreditAccountResponse)
async def update_credit(
    account_id: str,
    data: CreditUpdate,
    session: AsyncSession = Depends(get_session),
):
    result = await session.execute(
        select(CreditAccount)
        .options(selectinload(CreditAccount.items))
        .where(CreditAccount.id == account_id)
    )
    account = result.scalar_one_or_none()
    if not account:
        raise HTTPException(status_code=404, detail="Customer not found")

    account.customer_name = data.customer_name
    account.phone = data.phone
    account.id_number = data.id_number

    # delete old items
    for old_item in account.items:
        await session.delete(old_item)

    total_amount = 0.0
    total_paid = 0.0

    for item in data.items:
        balance = item.amount - item.paid_amount
        new_item = CreditItem(
            id=str(uuid.uuid4()),
            account_id=account_id,
            product_name=item.product_name,
            quantity=item.quantity,
            amount=item.amount,
            paid_amount=item.paid_amount,
            balance=balance,
            sale_date=item.sale_date,
            due_date=item.due_date,
            notes=item.notes,
        )
        session.add(new_item)
        total_amount += item.amount
        total_paid += item.paid_amount

    account.total_amount = total_amount
    account.total_paid = total_paid
    account.balance = total_amount - total_paid
    account.status = compute_status(total_amount, total_paid)

    await session.commit()

    result = await session.execute(
        select(CreditAccount)
        .options(selectinload(CreditAccount.items))
        .where(CreditAccount.id == account_id)
    )
    return result.scalar_one()


# =========================================
# DELETE CREDIT ACCOUNT
# =========================================

@router.delete("/{account_id}")
async def delete_credit(
    account_id: str,
    session: AsyncSession = Depends(get_session),
):
    result = await session.execute(
        select(CreditAccount).where(CreditAccount.id == account_id)
    )
    account = result.scalar_one_or_none()
    if not account:
        raise HTTPException(status_code=404, detail="Customer not found")

    await session.delete(account)
    await session.commit()
    return {"message": "Credit account deleted"}


# =========================================
# ADD ITEM TO EXISTING CUSTOMER
# =========================================

@router.post("/{account_id}/items", response_model=CreditAccountResponse)
async def add_item_to_credit(
    account_id: str,
    item: CreditItemCreate,
    session: AsyncSession = Depends(get_session),
):
    result = await session.execute(
        select(CreditAccount)
        .options(selectinload(CreditAccount.items))
        .where(CreditAccount.id == account_id)
    )
    account = result.scalar_one_or_none()
    if not account:
        raise HTTPException(status_code=404, detail="Customer not found")

    balance = item.amount - item.paid_amount
    new_item = CreditItem(
        id=str(uuid.uuid4()),
        account_id=account_id,
        product_name=item.product_name,
        quantity=item.quantity,
        amount=item.amount,
        paid_amount=item.paid_amount,
        balance=balance,
        sale_date=item.sale_date,
        due_date=item.due_date,
        notes=item.notes,
    )
    session.add(new_item)

    account.total_amount += item.amount
    account.total_paid += item.paid_amount
    account.balance = account.total_amount - account.total_paid
    account.status = compute_status(account.total_amount, account.total_paid)

    await session.commit()

    result = await session.execute(
        select(CreditAccount)
        .options(selectinload(CreditAccount.items))
        .where(CreditAccount.id == account_id)
    )
    return result.scalar_one()