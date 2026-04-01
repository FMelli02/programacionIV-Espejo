from typing import List, Optional

from sqlmodel import Session, select

from .models import Producto
from .schemas import ProductoCreate


def crear(session: Session, data: ProductoCreate) -> Producto:
    nuevo = Producto(**data.model_dump())
    session.add(nuevo)
    session.commit()
    session.refresh(nuevo)
    return nuevo


def obtener_todos(session: Session, skip: int, limit: int) -> List[Producto]:
    statement = select(Producto).offset(skip).limit(limit)
    return list(session.exec(statement).all())


def obtener_por_id(session: Session, id: int) -> Optional[Producto]:
    return session.get(Producto, id)


def actualizar_total(session: Session, id: int, data: ProductoCreate) -> Optional[Producto]:
    # Reemplazo total: Requiere todos los campos validables (ProductoCreate)
    producto = session.get(Producto, id)
    if not producto:
        return None

    for field, value in data.model_dump().items():
        setattr(producto, field, value)

    session.add(producto)
    session.commit()
    session.refresh(producto)
    return producto


def desactivar(session: Session, id: int) -> Optional[Producto]:
    # Borrado lógico: Solo altera el estado 'activo'
    producto = session.get(Producto, id)
    if not producto:
        return None

    producto.activo = False
    session.add(producto)
    session.commit()
    session.refresh(producto)
    return producto


def obtener_estado_stock(session: Session, id: int) -> Optional[dict]:
    producto = obtener_por_id(session, id)
    if not producto:
        return None

    # La lógica de negocio vive aquí
    alerta_stock = producto.stock < producto.stock_minimo

    return {
        "stock": producto.stock,
        "bajo_stock_minimo": alerta_stock,
        "activo": producto.activo,
    }
