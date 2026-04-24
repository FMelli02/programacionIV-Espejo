from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime, timezone

class ProductoCategoriaBase(SQLModel):
    es_principal: bool = Field(default=False)

class ProductoCategoria(ProductoCategoriaBase, table=True):
    producto_id: int = Field(primary_key=True, foreign_key="producto.id")
    categoria_id: int = Field(primary_key=True, foreign_key="categoria.id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
