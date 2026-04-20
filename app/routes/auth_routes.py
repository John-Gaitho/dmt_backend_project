from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from datetime import datetime, timedelta
import jwt

from app.database import get_session
from app.models.user import User
from app.config import settings

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# 🔐 Create JWT Token
def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        hours=settings.JWT_EXPIRY_HOURS
    )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )

    return encoded_jwt


# 🧾 Signup
@router.post("/signup")
async def signup(
    email: str,
    password: str,
    session: AsyncSession = Depends(get_session)
):

    result = await session.execute(
        select(User).where(User.email == email)
    )

    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="User already exists"
        )

    new_user = User(
        email=email,
        password=password
    )

    session.add(new_user)

    await session.commit()

    return {
        "message": "User created successfully"
    }


# 🔐 Signin (Login)
@router.post("/signin")
async def signin(
    email: str,
    password: str,
    session: AsyncSession = Depends(get_session)
):

    result = await session.execute(
        select(User).where(User.email == email)
    )

    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if user.password != password:
        raise HTTPException(
            status_code=401,
            detail="Incorrect password"
        )

    # Create token
    access_token = create_access_token(
        data={
            "sub": user.email
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }