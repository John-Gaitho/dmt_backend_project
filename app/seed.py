import asyncio

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import engine
from app.models.base import Base

# Import models
from app.models.user import User
from app.models.product import Product
from app.models.sale import Sale
from app.models.sale_item import SaleItem

from app.utils.security import hash_password


async def seed_data():

    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSession(engine) as session:

        print("🌱 Starting seed process...")

        # ===================================
        # 1. Create Admin User
        # ===================================

        result = await session.execute(
            select(User).where(
                User.email == "admin@dmt.com"
            )
        )

        admin = result.scalar_one_or_none()

        if not admin:

            admin = User(
                email="admin@dmt.com",
                password_hash=hash_password("123456")
            )

            session.add(admin)

            await session.commit()

            print("✅ Admin user created")

        else:
            print("ℹ️ Admin already exists")

        # ===================================
        # 2. Create Products WITH Images
        # ===================================

        products_data = [

            {
                "name": "Brake Pads",
                "description": "Toyota brake pads - high durability",
                "price": 2500,
                "image_url": "https://images.unsplash.com/photo-1615906655593-ad0386982a0f"
            },

            {
                "name": "Oil Filter",
                "description": "Premium engine oil filter",
                "price": 800,
                "image_url": "https://images.unsplash.com/photo-1581092335397-9583eb92d232"
            },

            {
                "name": "Spark Plug",
                "description": "NGK high-performance spark plug",
                "price": 450,
                "image_url": "https://images.unsplash.com/photo-1605731414532-6b26976cc153"
            },

            {
                "name": "Air Filter",
                "description": "Toyota air filter - dust protection",
                "price": 1200,
                "image_url": "https://images.unsplash.com/photo-1581093458791-9d15482442f7"
            },

            {
                "name": "Fuel Pump",
                "description": "Electric fuel pump assembly",
                "price": 6500,
                "image_url": "https://images.unsplash.com/photo-1592853625511-ad8c2f8a9e89"
            },

            {
                "name": "Radiator",
                "description": "Heavy-duty aluminum radiator",
                "price": 9500,
                "image_url": "https://images.unsplash.com/photo-1625047509168-a7026f36de04"
            },

            {
                "name": "Clutch Kit",
                "description": "Complete clutch replacement kit",
                "price": 13500,
                "image_url": "https://images.unsplash.com/photo-1619642751034-765dfdf7c58e"
            },

            {
                "name": "Timing Belt",
                "description": "OEM quality timing belt",
                "price": 4200,
                "image_url": "https://images.unsplash.com/photo-1621440318464-e05c7f0c93c3"
            },

            {
                "name": "Shock Absorber",
                "description": "Front shock absorber - smooth ride",
                "price": 7200,
                "image_url": "https://images.unsplash.com/photo-1621016450333-fbb35e6f1a03"
            },

            {
                "name": "Battery 12V",
                "description": "Heavy-duty car battery 12V",
                "price": 11500,
                "image_url": "https://images.unsplash.com/photo-1587202372775-e229f172b9d7"
            }

        ]

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

        await session.commit()

        print("✅ Products added")

        # ===================================
        # 3. Create Sample Sale
        # ===================================

        result = await session.execute(
            select(Product)
        )

        products = result.scalars().all()

        if products:

            sale = Sale(
                total_amount=3300
            )

            session.add(sale)

            await session.flush()

            sale_item = SaleItem(
                sale_id=sale.id,
                product_id=products[0].id,
                quantity=2,
                price=1650
            )

            session.add(sale_item)

            await session.commit()

            print("✅ Sample sale created")

        else:

            print("⚠️ No products found")

        print("🎉 Seed data completed")


if __name__ == "__main__":
    asyncio.run(seed_data())