from typing import Optional, List
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship


class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    price: float

    order_items: List["OrderItem"] = Relationship(back_populates="product")


class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_email: str
    total_amount: float = Field(default=0.0)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    items: List["OrderItem"] = Relationship(back_populates="order")


class OrderItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: Optional[int] = Field(default=None, foreign_key="order.id")
    product_id: Optional[int] = Field(default=None, foreign_key="product.id")
    quantity: int
    unit_price: float

    order: Optional[Order] = Relationship(back_populates="items")
    product: Optional[Product] = Relationship(back_populates="order_items")
