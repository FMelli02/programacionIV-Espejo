from pydantic import BaseModel, Field
from typing import Optional, List
from decimal import Decimal

class DetallePedidoCreate(BaseModel):
    producto_id: int
    cantidad: int
    precio_snapshot: Decimal = Field(max_digits=10, decimal_places=2)
    personalizacion: Optional[List[int]] = None

class PedidoBase(BaseModel):
    usuario_id: int
    direccion_id: Optional[int] = None
    estado_codigo: str
    forma_pago_codigo: str
    descuento: Decimal = Field(default=0.00, max_digits=10, decimal_places=2)
    costo_envio: Decimal = Field(default=50.00, max_digits=10, decimal_places=2)
    notas: Optional[str] = None

class PedidoCreate(PedidoBase):
    detalles: List[DetallePedidoCreate]

class PedidoUpdate(BaseModel):
    estado_codigo: Optional[str] = None
    forma_pago_codigo: Optional[str] = None
    notas: Optional[str] = None

class DetallePedidoResponse(BaseModel):
    pedido_id: int
    producto_id: int
    cantidad: int
    nombre_snapshot: str
    precio_snapshot: Decimal
    subtotal_snap: Decimal
    personalizacion: Optional[List[int]] = None

class PedidoResponse(PedidoBase):
    id: int
    subtotal: Decimal
    total: Decimal
    # detalles: List[DetallePedidoResponse] = []
