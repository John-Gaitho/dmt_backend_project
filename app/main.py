from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.database import engine
from app.models.base import Base

# Import models (important so tables exist)
from app.models import product
from app.models import sale
from app.models import sale_item
from app.models import user

# Import routes
from app.routes import product_routes
from app.routes import sales_routes
from app.routes import auth_routes
from app.routes import upload_routes

app = FastAPI(
    title="DMT Backend API",
    version="1.0.0"
)

# =========================
# ✅ CORS — MUST BE FIRST
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all during development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# ✅ Static Upload Folder
# =========================

app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads"
)

# =========================
# ✅ Create Database Tables
# =========================

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    print("✅ Database tables created successfully")


# =========================
# Root Test
# =========================

@app.get("/")
def root():
    return {"message": "DMT Backend Running 🚀"}


# =========================
# Register Routers
# =========================

app.include_router(product_routes.router)
app.include_router(sales_routes.router)
app.include_router(auth_routes.router)
app.include_router(upload_routes.router)