from sqlmodel import Session, select
from fastapi import HTTPException
from app.producto.model import Producto
from app.producto.schema import ProductoCreate, ProductoUpdate
from datetime import datetime, timezone

def listar_productos(session: Session) -> list[Producto]:
    return session.exec(select(Producto).where(Producto.deleted_at == None)).all()

def obtener_producto(producto_id: int, session: Session) -> Producto:
    producto = session.get(Producto, producto_id)
    if not producto or producto.deleted_at is not None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

def crear_producto(payload: ProductoCreate, session: Session) -> Producto:
    producto = Producto(**payload.model_dump())
    session.add(producto)
    session.commit()
    session.refresh(producto)
    return producto

def actualizar_producto(producto_id: int, payload: ProductoUpdate, session: Session) -> Producto:
    producto = obtener_producto(producto_id, session)
    producto_data = payload.model_dump(exclude_unset=True)
    for key, value in producto_data.items():
        setattr(producto, key, value)
    producto.updated_at = datetime.now(timezone.utc)
    session.add(producto)
    session.commit()
    session.refresh(producto)
    return producto

def eliminar_producto(producto_id: int, session: Session) -> None:
    producto = obtener_producto(producto_id, session)
    producto.deleted_at = datetime.now(timezone.utc)
    session.add(producto)
    session.commit()
