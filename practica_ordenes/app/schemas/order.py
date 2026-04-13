from typing import List
from pydantic import field_validator
from sqlmodel import SQLModel
from app.schemas.product import ProductRead


# ── Input ──────────────────────────────────────────────────────────────────────

class OrderItemCreate(SQLModel):
    product_id: int
    quantity: int

    @field_validator("quantity")
    @classmethod
    def quantity_must_be_positive(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("La cantidad debe ser mayor a 0")
        return v


class OrderCreate(SQLModel):
    user_email: str
    items: List[OrderItemCreate]


# ── Output ─────────────────────────────────────────────────────────────────────

class OrderItemRead(SQLModel):
    product_id: int
    quantity: int
    unit_price: float


class OrderItemDetailRead(SQLModel):
    """OrderItem con información completa del producto (usado en GET /orders/{id})."""
    product_id: int
    quantity: int
    unit_price: float
    product: ProductRead


class OrderRead(SQLModel):
    id: int
    user_email: str
    total_amount: float
    items: List[OrderItemRead]


class OrderDetailRead(SQLModel):
    """Detalle completo de la orden incluyendo información del producto por item."""
    id: int
    user_email: str
    total_amount: float
    items: List[OrderItemDetailRead]


# ── Paginación ─────────────────────────────────────────────────────────────────

class PaginatedOrders(SQLModel):
    total: int
    data: List[OrderRead]
