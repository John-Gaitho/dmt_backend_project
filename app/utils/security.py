
import bcrypt
import jwt
from datetime import datetime, timedelta

from app.config import settings

def hash_password(password: str):
    return bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()

def verify_password(password, hashed):
    return bcrypt.checkpw(
        password.encode(),
        hashed.encode()
    )

def create_token(user_id):
    payload = {
        "sub": str(user_id),
        "exp": datetime.utcnow()
        + timedelta(hours=settings.JWT_EXPIRY_HOURS)
    }

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
