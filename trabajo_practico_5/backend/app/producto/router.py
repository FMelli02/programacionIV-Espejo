from fastapi import APIRouter, status, Depends
from sqlmodel import Session
from app.core.database import get_session
from app.producto.schema import Producto, ProductoCreate, ProductoUpdate
from app.producto.service import (
    actualizar_producto,
    crear_producto,
    eliminar_producto,
    listar_productos,
)

router = APIRouter(prefix="/productos", tags=["Productos"])

@router.get("", response_model=list[Producto])
def get_productos(session: Session = Depends(get_session)) -> list[Producto]:
    return listar_productos(session)

@router.post("", response_model=Producto, status_code=status.HTTP_201_CREATED)
def post_producto(payload: ProductoCreate, session: Session = Depends(get_session)) -> Producto:
    return crear_producto(payload, session)

@router.put("/{producto_id}", response_model=Producto)
def put_producto(producto_id: int, payload: ProductoUpdate, session: Session = Depends(get_session)) -> Producto:
    return actualizar_producto(producto_id, payload, session)

@router.delete("/{producto_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_producto(producto_id: int, session: Session = Depends(get_session)) -> None:
    eliminar_producto(producto_id, session)
