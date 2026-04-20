from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession
)

from sqlalchemy.orm import declarative_base
from app.config import settings

# Create engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True
)

# Session maker
async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# VERY IMPORTANT — this enables tables
Base = declarative_base()

# Dependency
async def get_session():
    async with async_session() as session:
        yield session