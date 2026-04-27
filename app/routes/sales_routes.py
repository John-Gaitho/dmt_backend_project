from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.sale import Sale
from app.schemas.sale import (
    SaleCreate,
    SaleResponse
)

router = APIRouter(
    prefix="/sales",
    tags=["Sales"]
)


@router.post(
    "/",
    response_model=SaleResponse
)
def create_sale(
    sale: SaleCreate,
    db: Session = Depends(get_db)
):

    db_sale = Sale(
        **sale.dict()
    )

    db.add(db_sale)

    db.commit()

    db.refresh(db_sale)

    return db_sale