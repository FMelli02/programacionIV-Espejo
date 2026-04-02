from fastapi import HTTPException

from app.core.database import categorias_db, producto_categorias_db, productos_db
from app.producto_categoria.model import ProductoCategoriaModel
from app.producto_categoria.schema import ProductoCategoriaCreate


def listar_relaciones() -> list[ProductoCategoriaModel]:
    return producto_categorias_db


def crear_relacion(payload: ProductoCategoriaCreate) -> ProductoCategoriaModel:
    existe_producto = any(prod.id == payload.productoid for prod in productos_db)
    existe_categoria = any(cat.id == payload.categoriaid for cat in categorias_db)

    if not existe_producto or not existe_categoria:
        raise HTTPException(
            status_code=404,
            detail="Producto o categoría inexistente",
        )

    ya_existe = any(
        rel.productoid == payload.productoid and rel.categoriaid == payload.categoriaid
        for rel in producto_categorias_db
    )
    if ya_existe:
        raise HTTPException(status_code=409, detail="La relación ya existe")

    nueva_relacion = ProductoCategoriaModel(
        productoid=payload.productoid,
        categoriaid=payload.categoriaid,
    )
    producto_categorias_db.append(nueva_relacion)
    return nueva_relacion


def eliminar_relacion(productoid: int, categoriaid: int) -> None:
    relacion = next(
        (
            rel
            for rel in producto_categorias_db
            if rel.productoid == productoid and rel.categoriaid == categoriaid
        ),
        None,
    )

    if relacion is None:
        raise HTTPException(status_code=404, detail="Relación no encontrada")

    producto_categorias_db.remove(relacion)
