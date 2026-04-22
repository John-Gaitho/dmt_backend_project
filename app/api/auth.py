from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_session
from app.models.user import User

from app.utils.security import (
    hash_password,
    verify_password,
    create_token
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

# ============================
# SIGNUP
# ============================

@router.post("/signup")
async def signup(
    data: dict,
    db: AsyncSession = Depends(get_session)
):

    email = data.get("email")
    password = data.get("password")

    if not email or not password:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email and password required"
        )

    # Check if user exists

    result = await db.execute(
        select(User).where(
            User.email == email
        )
    )

    existing_user = result.scalar_one_or_none()

    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="User already exists"
        )

    # Create user

    user = User(

        email=email,

        password_hash=
            hash_password(password),

        is_admin=False  # default

    )

    db.add(user)

    await db.commit()

    await db.refresh(user)

    # Create token with admin flag

    token = create_token(user)

    return {

        "access_token": token,

        "user": {

            "id": user.id,

            "email": user.email,

            "is_admin": user.is_admin

        }

    }


# ============================
# SIGNIN
# ============================

@router.post("/signin")
async def signin(
    data: dict,
    db: AsyncSession = Depends(get_session)
):

    email = data.get("email")
    password = data.get("password")

    if not email or not password:

        raise HTTPException(
            status_code=400,
            detail="Email and password required"
        )

    result = await db.execute(
        select(User).where(
            User.email == email
        )
    )

    user = result.scalar_one_or_none()

    if not user:

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(
        password,
        user.password_hash
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # Create JWT with admin role

    token = create_token(user)

    return {

        "access_token": token,

        "user": {

            "id": user.id,

            "email": user.email,

            "is_admin": user.is_admin

        }

    }