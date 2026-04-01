from typing import Optional

from sqlmodel import Field, SQLModel


class Categoria(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    codigo: str
    descripcion: str
    activo: bool = True
