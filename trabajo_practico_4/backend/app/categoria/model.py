from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime, timezone

class CategoriaBase(SQLModel):
    parent_id: Optional[int] = Field(default=None, foreign_key="categoria.id")
    nombre: str = Field(max_length=100, unique=True, index=True)
    descripcion: Optional[str] = None
    imagen_url: Optional[str] = None

class Categoria(CategoriaBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    deleted_at: Optional[datetime] = None
