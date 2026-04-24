from pydantic import BaseModel, Field
from decimal import Decimal
from typing import Optional

class ProductoBase(BaseModel):
    nombre: str = Field(min_length=2, max_length=150)
    descripcion: Optional[str] = None
    precio_base: Decimal
    imagenes_url: Optional[list[str]] = Field(default_factory=list)
    stock_cantidad: int = 0
    disponible: bool = True

class ProductoCreate(ProductoBase):
    pass

class ProductoUpdate(ProductoBase):
    pass

class Producto(ProductoBase):
    id: int
