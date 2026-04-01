from typing import Optional

from sqlmodel import Field, SQLModel


class Cliente(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    email: str = Field(index=True)
    ciudad: str
    edad: int
    limite_credito: float
    saldo_pendiente: float = 0
    activo: bool = True
    riesgo_credito: str
