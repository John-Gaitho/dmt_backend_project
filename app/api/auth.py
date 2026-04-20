
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_session
from app.models.user import User
from app.utils.security import (
    hash_password,
    verify_password,
    create_token
)

router = APIRouter()

@router.post("/signup")
async def signup(data: dict,
                 db: AsyncSession = Depends(get_session)):

    email = data["email"]
    password = data["password"]

    result = await db.execute(
        select(User).where(
            User.email == email
        )
    )

    if result.scalar():
        return {"error": "User exists"}

    user = User(
        email=email,
        password_hash=hash_password(password)
    )

    db.add(user)
    await db.commit()

    token = create_token(user.id)

    return {
        "access_token": token
    }


@router.post("/signin")
async def signin(data: dict,
                 db: AsyncSession = Depends(get_session)):

    email = data["email"]
    password = data["password"]

    result = await db.execute(
        select(User).where(
            User.email == email
        )
    )

    user = result.scalar()

    if not user:
        return {"error": "Invalid"}

    if not verify_password(
            password,
            user.password_hash):
        return {"error": "Invalid"}

    token = create_token(user.id)

    return {
        "access_token": token
    }
