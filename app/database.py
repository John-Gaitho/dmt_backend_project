from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

from app.config import settings

# =========================
# ENGINE
# =========================
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,
    future=True
)

# =========================
# SESSION
# =========================
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# =========================
# BASE
# =========================
Base = declarative_base()

# =========================
# MODELS IMPORT (IMPORTANT)
# =========================
from app.models.product import Product  # noqa
from app.models.credit import CreditAccount, CreditItem
from app.models.sale import Sale  # noqa
from app.models.order import Order  # noqa
from app.models.user import User  # noqa
from app.models.order_item import OrderItem

# =========================
# DEPENDENCY
# =========================
async def get_session():
    async with AsyncSessionLocal() as session:
        yield session