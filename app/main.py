from fastapi import FastAPI

from app.database import engine
from app.models.base import Base

# Import models
from app.models import product
from app.models import sale
from app.models import sale_item

# Import routes
from app.routes import product_routes
from app.routes import sales_routes
from app.routes import auth_routes
from app.routes import upload_routes

app = FastAPI()


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    print("✅ Database tables created successfully")


@app.get("/")
def root():
    return {"message": "DMT Backend Running 🚀"}


# Register routes
app.include_router(product_routes.router)
app.include_router(sales_routes.router)
app.include_router(auth_routes.router)
app.include_router(upload_routes.router)