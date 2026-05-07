
import asyncio
import uuid
from random import choice, randint

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import engine
from app.models.base import Base

from app.models.user import User
from app.models.product import Product
from app.models.order import Order
from app.models.order_item import OrderItem

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
        # ADMIN USER
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
                "stock_quantity": 50,
                "in_stock": True
            },
            {
                "name": "Oil Filter",
                "price": 800,
                "category": "Engine",
                "description": "Premium engine oil filter",
                "image_urls": [
                    "https://images.unsplash.com/photo-1581092335397-9583eb92d232"
                ],
                "stock_quantity": 100,
                "in_stock": True
            },
            {
                "name": "Spark Plug",
                "price": 450,
                "category": "Engine",
                "description": "NGK spark plug",
                "image_urls": [
                    "https://images.unsplash.com/photo-1605731414532-6b26976cc153"
                ],
                "stock_quantity": 200,
                "in_stock": True
            },
            {
                "name": "Battery 12V",
                "price": 11500,
                "category": "Electrical",
                "description": "Heavy-duty automotive battery",
                "image_urls": [
                    "https://images.unsplash.com/photo-1587202372775-e229f172b9d7"
                ],
                "stock_quantity": 15,
                "in_stock": True
            },
        ]

        added_products = 0

        for pdata in products_data:
            result = await session.execute(
                select(Product).where(Product.name == pdata["name"])
            )
            existing = result.scalar_one_or_none()

            if not existing:
                session.add(Product(**pdata))
                added_products += 1

        await session.commit()
        print(f"✅ {added_products} Products added")

        # =========================
        # ORDERS + ITEMS
        # =========================
        print("📦 Seeding orders...")

        result = await session.execute(select(Product))
        products = result.scalars().all()

        if not products:
            print("⚠️ No products found, skipping orders...")
            return

        statuses = ["pending", "processing", "shipped", "delivered"]

        added_orders = 0

        for _ in range(10):

            num_items = randint(1, 3)
            selected_products = [
                choice(products) for _ in range(num_items)
            ]

            items = []
            total = 0

            for product in selected_products:

                quantity = randint(1, 5)
                price = float(product.price)

                item_total = price * quantity
                total += item_total

                items.append({
                    "product": product,
                    "quantity": quantity,
                    "price": price
                })

            # ✅ CREATE ORDER WITH FINAL TOTAL (NO ZERO STATE)
            order = Order(
                id=str(uuid.uuid4()),
                user_id=None,
                total_amount=round(total, 2),
                status=choice(statuses)
            )

            session.add(order)
            await session.flush()

            # ✅ CREATE ITEMS AFTER ORDER
            for item in items:
                session.add(
                    OrderItem(
                        id=str(uuid.uuid4()),
                        order_id=order.id,
                        product_id=item["product"].id,
                        quantity=item["quantity"],
                        price=item["price"]
                    )
                )

            added_orders += 1

        await session.commit()

        print(f"✅ {added_orders} Orders added")
        print("🎉 Seed completed successfully!")


if __name__ == "__main__":
    asyncio.run(seed_data())

