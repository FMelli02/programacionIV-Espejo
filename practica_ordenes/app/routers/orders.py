from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select, func

from app.database import get_session
from app.models import Order, OrderItem, Product
from app.schemas.order import (
    OrderCreate,
    OrderRead,
    OrderDetailRead,
    OrderItemDetailRead,
    PaginatedOrders,
)
from app.schemas.product import ProductRead

router = APIRouter(prefix="/orders", tags=["orders"])


# ── POST /orders ───────────────────────────────────────────────────────────────

@router.post("", response_model=OrderRead, status_code=201)
def create_order(order_in: OrderCreate, session: Session = Depends(get_session)):
    """
    Unit of Work: Todos los items están resueltos y persistidos automáticamente.
    Si algún producto no se encuentra en la transacción se vuelve atrás.
    """
    total = 0.0
    resolved_items: list[OrderItem] = []

    for item_in in order_in.items:
        product = session.get(Product, item_in.product_id)
        if product is None:
            raise HTTPException(status_code=404, detail="Producto no encontrado")

        unit_price = product.price
        total += unit_price * item_in.quantity
        resolved_items.append(
            OrderItem(
                product_id=item_in.product_id,
                quantity=item_in.quantity,
                unit_price=unit_price,
            )
        )

    order = Order(user_email=order_in.user_email, total_amount=total)
    session.add(order)
    session.flush()  # get order.id antes de añadir items

    for item in resolved_items:
        item.order_id = order.id
        session.add(item)

    session.commit()
    session.refresh(order)

    return OrderRead(
        id=order.id,
        user_email=order.user_email,
        total_amount=order.total_amount,
        items=[
            {"product_id": i.product_id, "quantity": i.quantity, "unit_price": i.unit_price}
            for i in order.items
        ],
    )


# ── GET /orders/{id} ───────────────────────────────────────────────────────────

@router.get("/{order_id}", response_model=OrderDetailRead)
def get_order(order_id: int, session: Session = Depends(get_session)):
    order = session.get(Order, order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Orden no encontrada")

    detail_items: list[OrderItemDetailRead] = []
    for item in order.items:
        product = session.get(Product, item.product_id)
        detail_items.append(
            OrderItemDetailRead(
                product_id=item.product_id,
                quantity=item.quantity,
                unit_price=item.unit_price,
                product=ProductRead(
                    id=product.id,
                    name=product.name,
                    price=product.price,
                ),
            )
        )

    return OrderDetailRead(
        id=order.id,
        user_email=order.user_email,
        total_amount=order.total_amount,
        items=detail_items,
    )


# ── GET /orders?offset=&limit= ─────────────────────────────────────────────────

@router.get("", response_model=PaginatedOrders)
def list_orders(
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
    session: Session = Depends(get_session),
):
    total = session.exec(select(func.count()).select_from(Order)).one()
    orders = session.exec(select(Order).offset(offset).limit(limit)).all()

    data = []
    for order in orders:
        data.append(
            OrderRead(
                id=order.id,
                user_email=order.user_email,
                total_amount=order.total_amount,
                items=[
                    {
                        "product_id": i.product_id,
                        "quantity": i.quantity,
                        "unit_price": i.unit_price,
                    }
                    for i in order.items
                ],
            )
        )

    return PaginatedOrders(total=total, data=data)
