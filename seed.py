import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import engine
from app.models.base import Base

from app.models.user import User
from app.models.product import Product

from app.utils.security import hash_password


async def seed_data():

    # =========================
    # CREATE TABLES
    # =========================
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSession(engine) as session:

        print("🌱 Starting seed process...")

        # =========================
        # CREATE ADMIN USER
        # =========================
        admin_email = "admin@dmt.com"

        result = await session.execute(
            select(User).where(User.email == admin_email)
        )

        admin = result.scalar_one_or_none()

        if not admin:

            admin = User(
                email=admin_email,
                password_hash=hash_password("123456"),
                is_admin=True
            )

            session.add(admin)
            await session.commit()

            print("✅ Admin created")

        else:
            print("ℹ️ Admin already exists")

        # =========================
        # PRODUCTS
        # =========================
        products_data = [

            {
                "name": "Brake Pads",
                "price": 2500,
                "category": "Brakes",
                "description": "Toyota brake pads set",
                "image_urls": [
                    "https://images.unsplash.com/photo-1615906655593-ad0386982a0f"
                ],
                "stock_quantity": 50
            },

            {
                "name": "Oil Filter",
                "price": 800,
                "category": "Engine",
                "description": "Premium engine oil filter",
                "image_urls": [
                    "https://images.unsplash.com/photo-1581092335397-9583eb92d232"
                ],
                "stock_quantity": 100
            },

            {
                "name": "Spark Plug",
                "price": 450,
                "category": "Engine",
                "description": "NGK spark plug",
                "image_urls": [
                    "https://images.unsplash.com/photo-1605731414532-6b26976cc153"
                ],
                "stock_quantity": 200
            },

            {
                "name": "Battery 12V",
                "price": 11500,
                "category": "Electrical",
                "description": "Heavy-duty automotive battery",
                "image_urls": [
                    "https://images.unsplash.com/photo-1587202372775-e229f172b9d7"
                ],
                "stock_quantity": 15
            },

            {
                "name": "Air Filter",
                "price": 1200,
                "category": "Engine",
                "description": "High-performance air filter",
                "image_urls": [
                    "https://images.unsplash.com/photo-1600959907703-125ba1374a12"
                ],
                "stock_quantity": 60
            },

            {
                "name": "Radiator",
                "price": 18500,
                "category": "Cooling",
                "description": "Durable aluminum radiator",
                "image_urls": [
                    "https://images.unsplash.com/photo-1625047509168-a7026f36de04"
                ],
                "stock_quantity": 10
            },

            {
                "name": "Clutch Plate",
                "price": 7200,
                "category": "Transmission",
                "description": "Heavy-duty clutch plate",
                "image_urls": [
                    "https://images.unsplash.com/photo-1621259182978-fbf93132d53d"
                ],
                "stock_quantity": 25
            }

        ]

        added_count = 0

        for pdata in products_data:

            result = await session.execute(
                select(Product).where(
                    Product.name == pdata["name"]
                )
            )

            existing = result.scalar_one_or_none()

            if not existing:
                product = Product(**pdata)
                session.add(product)
                added_count += 1

        await session.commit()

        print(f"✅ {added_count} Products added")
        print("🎉 Seed completed")


# =========================
# RUN
# =========================
if __name__ == "__main__":
    asyncio.run(seed_data())