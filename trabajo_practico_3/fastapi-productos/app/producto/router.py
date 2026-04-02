from fastapi import APIRouter, status

from app.producto.schema import Producto, ProductoCreate, ProductoUpdate
from app.producto.service import (
    actualizar_producto,
    crear_producto,
    eliminar_producto,
    listar_productos,
)


router = APIRouter(prefix="/productos", tags=["Productos"])


@router.get("", response_model=list[Producto])
def get_productos() -> list[Producto]:
    return listar_productos()


@router.post("", response_model=Producto, status_code=status.HTTP_201_CREATED)
def post_producto(payload: ProductoCreate) -> Producto:
    return crear_producto(payload)


@router.put("/{producto_id}", response_model=Producto)
def put_producto(producto_id: int, payload: ProductoUpdate) -> Producto:
    return actualizar_producto(producto_id, payload)


@router.delete("/{producto_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_producto(producto_id: int) -> None:
    eliminar_producto(producto_id)
