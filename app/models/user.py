import uuid

from sqlalchemy import (
    Column,
    String,
    DateTime,
    Boolean
)

from datetime import datetime

from app.models.base import Base


class User(Base):

    __tablename__ = "users"

    # Use String UUID (works for SQLite & PostgreSQL)
    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    email = Column(
        String,
        unique=True,
        nullable=False,
        index=True
    )

    password_hash = Column(
        String,
        nullable=False
    )

    # ✅ ADMIN ROLE SUPPORT
    is_admin = Column(
        Boolean,
        default=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    def __repr__(self):

        return f"<User {self.email}>"