from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession
)

from sqlalchemy.orm import declarative_base

from app.config import settings

# =========================
# DATABASE ENGINE
# =========================

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,
    future=True
)

# =========================
# SESSION FACTORY
# =========================

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# =========================
# BASE MODEL
# =========================

Base = declarative_base()

# =========================
# IMPORTANT: IMPORT MODELS
# Ensures SQLAlchemy sees all tables
# =========================

from app.models.product import Product      # noqa
from app.models.sale import Sale            # noqa
from app.models.order import Order          # noqa
from app.models.user import User            # noqa


# =========================
# DB SESSION DEPENDENCIES
# =========================

# ✅ Existing routes use this
async def get_session():
    async with AsyncSessionLocal() as session:
        yield session


# ✅ Future routes can use this
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session