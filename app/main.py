from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.database import engine, Base

from app.models.user import User
from app.models.credit import CreditAccount, CreditItem
from app.models.product import Product
from app.models.sale import Sale
from app.models.order import Order
from app.models.order_item import OrderItem
#import app.models

from app.routes import (
    credit_routes,
    product_routes,
    sales_routes,
    auth_routes,
    upload_routes,
    order_routes,
    order_item_routes,
)

app = FastAPI(title="DMT Backend API", version="1.0.0")

# =========================
# CORS
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# STATIC FILES
# =========================
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# =========================
# STARTUP
# =========================
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    print("✅ Database tables created successfully")

# =========================
# ROOT
# =========================
@app.get("/")
def root():
    return {"message": "DMT Backend Running 🚀"}

# =========================
# ROUTES
# =========================
app.include_router(product_routes.router)
app.include_router(sales_routes.router)
app.include_router(auth_routes.router)
app.include_router(upload_routes.router)
app.include_router(order_routes.router)
app.include_router(order_item_routes.router)

app.include_router(
    credit_routes.router,
    prefix="/credit-records",
    tags=["Credits"]
)