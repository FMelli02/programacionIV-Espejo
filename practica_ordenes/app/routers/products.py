from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.database import get_session
from app.models import Product
from app.schemas.product import ProductCreate, ProductRead

router = APIRouter(prefix="/products", tags=["products"])


@router.post("", response_model=ProductRead, status_code=201)
def create_product(product_in: ProductCreate, session: Session = Depends(get_session)):
    product = Product.model_validate(product_in)
    session.add(product)
    session.commit()
    session.refresh(product)
    return product
