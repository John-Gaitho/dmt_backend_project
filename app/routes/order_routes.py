from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uuid

from app.database import get_session
from app.models.order import Order
from app.schemas.order import OrderCreate, OrderUpdate

router = APIRouter(prefix="/orders", tags=["Orders"])


# =========================
# CREATE ORDER
# =========================
@router.post("/")
async def create_order(
    payload: OrderCreate,
    session: AsyncSession = Depends(get_session)
):
    order = Order(
        id=str(uuid.uuid4()),
        customer_name=payload.customer_name,
        total_amount=payload.total_amount,
        payment_method=payload.payment_method,
        status="pending"
    )

    session.add(order)
    await session.commit()
    await session.refresh(order)

    return order


# =========================
# GET ALL ORDERS
# =========================
@router.get("/")
async def get_orders(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Order))
    return result.scalars().all()


# =========================
# UPDATE ORDER STATUS
# =========================
@router.put("/{order_id}")
async def update_order(
    order_id: str,
    payload: OrderUpdate,
    session: AsyncSession = Depends(get_session)
):
    result = await session.execute(
        select(Order).where(Order.id == order_id)
    )

    order = result.scalar_one_or_none()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order.status = payload.status

    await session.commit()
    await session.refresh(order)

    return order


# =========================
# DELETE ORDER
# =========================
@router.delete("/{order_id}")
async def delete_order(
    order_id: str,
    session: AsyncSession = Depends(get_session)
):
    result = await session.execute(
        select(Order).where(Order.id == order_id)
    )

    order = result.scalar_one_or_none()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    await session.delete(order)
    await session.commit()

    return {"message": "Order deleted"}