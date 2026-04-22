import bcrypt
import jwt

from datetime import (
    datetime,
    timedelta
)

from app.config import settings


# =========================
# PASSWORD HASHING
# =========================

def hash_password(password: str) -> str:

    return bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()


def verify_password(
    password: str,
    hashed: str
) -> bool:

    return bcrypt.checkpw(
        password.encode(),
        hashed.encode()
    )


# =========================
# JWT TOKEN CREATION
# =========================

def create_token(user):

    """
    Accepts full user object
    Stores admin role inside JWT
    """

    payload = {

        # User ID
        "sub": str(user.id),

        # Email (useful in frontend)
        "email": user.email,

        # 🔥 IMPORTANT — Admin role
        "is_admin": user.is_admin,

        # Expiry
        "exp":
            datetime.utcnow()
            + timedelta(
                hours=settings.JWT_EXPIRY_HOURS
            )

    }

    token = jwt.encode(

        payload,

        settings.SECRET_KEY,

        algorithm=settings.JWT_ALGORITHM

    )

    return token


# =========================
# TOKEN DECODER (NEW)
# =========================

def decode_token(token: str):

    try:

        payload = jwt.decode(

            token,

            settings.SECRET_KEY,

            algorithms=[
                settings.JWT_ALGORITHM
            ]

        )

        return payload

    except jwt.ExpiredSignatureError:

        return None

    except jwt.InvalidTokenError:

        return None