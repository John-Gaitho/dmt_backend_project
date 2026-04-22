from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Header
)

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from pydantic import BaseModel

from datetime import (
    datetime,
    timedelta
)

import jwt

from app.database import get_session
from app.models.user import User
from app.config import settings

from app.utils.security import (
    hash_password,
    verify_password
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

# =========================
# Request Models
# =========================

class RegisterRequest(BaseModel):
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


# =========================
# Create JWT Token
# =========================

def create_access_token(user: User):

    payload = {

        # user id
        "sub": str(user.id),

        # email
        "email": user.email,

        # 🔥 REQUIRED
        "is_admin": user.is_admin,

        "exp":
            datetime.utcnow()
            + timedelta(
                hours=settings.JWT_EXPIRY_HOURS
            )
    }

    encoded_jwt = jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )

    return encoded_jwt


# =========================
# REGISTER
# =========================

@router.post("/register")
async def register(
    user: RegisterRequest,
    session: AsyncSession = Depends(get_session)
):

    result = await session.execute(
        select(User).where(
            User.email == user.email
        )
    )

    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="User already exists"
        )

    hashed_pw = hash_password(
        user.password
    )

    new_user = User(
        email=user.email,
        password_hash=hashed_pw
    )

    session.add(new_user)

    await session.commit()

    return {
        "message": "User created successfully"
    }


# =========================
# LOGIN
# =========================

@router.post("/login")
async def login(
    user: LoginRequest,
    session: AsyncSession = Depends(get_session)
):

    result = await session.execute(
        select(User).where(
            User.email == user.email
        )
    )

    db_user = result.scalar_one_or_none()

    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if not verify_password(
        user.password,
        db_user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Incorrect password"
        )

    # ✅ FIXED
    access_token = create_access_token(
        db_user
    )

    return {

        "access_token": access_token,

        "token_type": "bearer"

    }


# =========================
# 🔥 REQUIRED — GET CURRENT USER
# =========================

@router.get("/me")
async def get_current_user(

    authorization: str = Header(None),

    session: AsyncSession = Depends(get_session)

):

    if not authorization:

        raise HTTPException(
            status_code=401,
            detail="Missing token"
        )

    token = authorization.replace(
        "Bearer ",
        ""
    )

    try:

        payload = jwt.decode(

            token,

            settings.SECRET_KEY,

            algorithms=[
                settings.JWT_ALGORITHM
            ]

        )

    except jwt.ExpiredSignatureError:

        raise HTTPException(
            status_code=401,
            detail="Token expired"
        )

    except jwt.InvalidTokenError:

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    user_id = payload.get("sub")

    result = await session.execute(

        select(User).where(
            User.id == user_id
        )

    )

    user = result.scalar_one_or_none()

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {

        "id": str(user.id),

        "email": user.email,

        "is_admin": user.is_admin

    }