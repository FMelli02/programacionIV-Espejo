from typing import Optional
from sqlmodel import SQLModel, Field, Column
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import String
from decimal import Decimal
from datetime import datetime, timezone

class FormaPagoBase(SQLModel):
    codigo: str = Field(primary_key=True, max_length=20)
    descripcion: str = Field(max_length=80)
    habilitado: bool = Field(default=True)

class FormaPago(FormaPagoBase, table=True):
    pass

class EstadoPedidoBase(SQLModel):
    codigo: str = Field(primary_key=True, max_length=20)
    descripcion: str = Field(max_length=80)
    orden: int
    es_terminal: bool

class EstadoPedido(EstadoPedidoBase, table=True):
    pass

class PedidoBase(SQLModel):
    usuario_id: int
    direccion_id: Optional[int] = None
    estado_codigo: str = Field(foreign_key="estadopedido.codigo")
    forma_pago_codigo: str = Field(foreign_key="formapago.codigo")
    subtotal: Decimal = Field(max_digits=10, decimal_places=2)
    descuento: Decimal = Field(default=0.00, max_digits=10, decimal_places=2)
    costo_envio: Decimal = Field(default=50.00, max_digits=10, decimal_places=2)
    total: Decimal = Field(max_digits=10, decimal_places=2)
    notas: Optional[str] = None

class Pedido(PedidoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    deleted_at: Optional[datetime] = None

class DetallePedidoBase(SQLModel):
    cantidad: int
    nombre_snapshot: str = Field(max_length=200)
    precio_snapshot: Decimal = Field(max_digits=10, decimal_places=2)
    subtotal_snap: Decimal = Field(max_digits=10, decimal_places=2)
    personalizacion: Optional[list[int]] = Field(default=None, sa_column=Column(ARRAY(String)))

class DetallePedido(DetallePedidoBase, table=True):
    pedido_id: int = Field(primary_key=True, foreign_key="pedido.id")
    producto_id: int = Field(primary_key=True, foreign_key="producto.id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class HistorialEstadoPedidoBase(SQLModel):
    estado_desde: Optional[str] = Field(default=None, foreign_key="estadopedido.codigo")
    estado_hacia: str = Field(foreign_key="estadopedido.codigo")
    usuario_id: Optional[int] = None
    motivo: Optional[str] = None

class HistorialEstadoPedido(HistorialEstadoPedidoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    pedido_id: int = Field(foreign_key="pedido.id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class PagoBase(SQLModel):
    mp_payment_id: Optional[int] = Field(default=None, unique=True)
    mp_status: str = Field(max_length=30)
    mp_status_detail: Optional[str] = Field(default=None, max_length=100)
    external_reference: str = Field(max_length=100, unique=True)
    idempotency_key: str = Field(max_length=100, unique=True)
    transaction_amount: Decimal = Field(max_digits=10, decimal_places=2)
    payment_method_id: Optional[str] = Field(default=None, max_length=50)

class Pago(PagoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    pedido_id: int = Field(foreign_key="pedido.id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
