from typing import Optional
from sqlmodel import SQLModel, Field, Column
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import String
from decimal import Decimal
from datetime import datetime, timezone

class ProductoBase(SQLModel):
    nombre: str = Field(max_length=150)
    descripcion: Optional[str] = None
    precio_base: Decimal = Field(max_digits=10, decimal_places=2)
    imagenes_url: Optional[list[str]] = Field(default=None, sa_column=Column(ARRAY(String)))
    stock_cantidad: int = Field(default=0)
    disponible: bool = Field(default=True)

class Producto(ProductoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    deleted_at: Optional[datetime] = None
