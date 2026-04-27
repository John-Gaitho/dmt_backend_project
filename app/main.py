from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.database import engine
from app.models.base import Base

# =========================
# Models (ensure tables register)
# =========================
from app.models import (
    product,
    sale,
    user,
    order,
    order_item,
)

# =========================
# Routes
# =========================
from app.routes import (
    product_routes,
    sales_routes,
    auth_routes,
    upload_routes,
    order_routes,
    order_item_routes,
)

# =========================
# FastAPI app
# =========================
app = FastAPI(
    title="DMT Backend API",
    version="1.0.0",
)

# =========================
# CORS
# =========================
origins = [
    "http://localhost:8080",
]



app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # dev only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# Static files (uploads)
# =========================
app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads"
)

# =========================
# Startup (create tables)
# =========================
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    print("✅ Database tables created successfully")

# =========================
# Root endpoint
# =========================
@app.get("/")
def root():
    return {"message": "DMT Backend Running 🚀"}

# =========================
# Routers
# =========================
app.include_router(product_routes.router)
app.include_router(sales_routes.router)
app.include_router(auth_routes.router)
app.include_router(upload_routes.router)
app.include_router(order_routes.router)
app.include_router(order_item_routes.router)
