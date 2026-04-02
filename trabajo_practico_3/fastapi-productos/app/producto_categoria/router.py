from fastapi import APIRouter, status

from app.producto_categoria.schema import ProductoCategoria, ProductoCategoriaCreate
from app.producto_categoria.service import (
    crear_relacion,
    eliminar_relacion,
    listar_relaciones,
)


router = APIRouter(prefix="/producto-categorias", tags=["ProductoCategorias"])


@router.get("", response_model=list[ProductoCategoria])
def get_producto_categorias() -> list[ProductoCategoria]:
    return listar_relaciones()


@router.post(
    "",
    response_model=ProductoCategoria,
    status_code=status.HTTP_201_CREATED,
)
def post_producto_categoria(payload: ProductoCategoriaCreate) -> ProductoCategoria:
    return crear_relacion(payload)


@router.delete("/{productoid}/{categoriaid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_producto_categoria(productoid: int, categoriaid: int) -> None:
    eliminar_relacion(productoid, categoriaid)
