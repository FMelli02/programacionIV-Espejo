from fastapi import HTTPException

from app.core.database import productos_db, siguiente_id_productos
from app.producto.model import ProductoModel
from app.producto.schema import ProductoCreate, ProductoUpdate


def listar_productos() -> list[ProductoModel]:
    return productos_db


def obtener_producto(producto_id: int) -> ProductoModel:
    producto = next((prod for prod in productos_db if prod.id == producto_id), None)
    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto


def crear_producto(payload: ProductoCreate) -> ProductoModel:
    nuevo_producto = ProductoModel(
        id=siguiente_id_productos(),
        nombre=payload.nombre,
        descripcion=payload.descripcion,
        preciobase=payload.preciobase,
        imagenurl=payload.imagenurl,
        disponible=payload.disponible,
    )
    productos_db.append(nuevo_producto)
    return nuevo_producto


def actualizar_producto(producto_id: int, payload: ProductoUpdate) -> ProductoModel:
    producto = obtener_producto(producto_id)
    producto.nombre = payload.nombre
    producto.descripcion = payload.descripcion
    producto.preciobase = payload.preciobase
    producto.imagenurl = payload.imagenurl
    producto.disponible = payload.disponible
    return producto


def eliminar_producto(producto_id: int) -> None:
    producto = obtener_producto(producto_id)
    productos_db.remove(producto)
