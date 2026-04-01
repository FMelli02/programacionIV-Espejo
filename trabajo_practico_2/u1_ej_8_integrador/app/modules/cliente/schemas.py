from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class ClienteBase(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=60, example="Lucia Fernandez")
    email: str = Field(..., min_length=6, max_length=120, example="lucia@email.com")
    ciudad: str = Field(..., min_length=2, max_length=40, example="Cordoba")
    edad: int = Field(..., ge=18, le=99, example=30)
    limite_credito: float = Field(..., gt=0, example=150000)
    saldo_pendiente: float = Field(0, ge=0, example=5000)
    activo: bool = True

    @field_validator("nombre")
    @classmethod
    def validar_nombre(cls, value: str) -> str:
        normalizado = " ".join(value.strip().split())
        if len(normalizado) < 3:
            raise ValueError("El nombre debe tener al menos 3 caracteres")
        return normalizado

    @field_validator("email")
    @classmethod
    def validar_email(cls, value: str) -> str:
        normalizado = value.strip().lower()
        if "@" not in normalizado or "." not in normalizado.split("@")[-1]:
            raise ValueError("El email no tiene un formato valido")
        return normalizado

    @model_validator(mode="after")
    def validar_credito(self):
        if self.saldo_pendiente > self.limite_credito:
            raise ValueError("El saldo pendiente no puede superar el limite de credito")
        return self


class ClienteCreate(ClienteBase):
    pass


class ClienteUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=3, max_length=60)
    email: Optional[str] = Field(None, min_length=6, max_length=120)
    ciudad: Optional[str] = Field(None, min_length=2, max_length=40)
    edad: Optional[int] = Field(None, ge=18, le=99)
    limite_credito: Optional[float] = Field(None, gt=0)
    saldo_pendiente: Optional[float] = Field(None, ge=0)
    activo: Optional[bool] = None


class ClienteRead(ClienteBase):
    id: int
    riesgo_credito: str

    model_config = ConfigDict(from_attributes=True)


class ClienteSaldoResponse(BaseModel):
    saldo_pendiente: float
    limite_credito: float
    riesgo_credito: str
