from fastapi import APIRouter, status, Depends
from sqlmodel import Session
from app.core.database import get_session
from app.producto_categoria.schema import ProductoCategoria, ProductoCategoriaCreate
from app.producto_categoria.service import (
    crear_relacion,
    eliminar_relacion,
    listar_relaciones,
)

router = APIRouter(prefix="/producto-categorias", tags=["ProductoCategorias"])

@router.get("", response_model=list[ProductoCategoria])
def get_producto_categorias(session: Session = Depends(get_session)) -> list[ProductoCategoria]:
    return listar_relaciones(session)

@router.post(
    "",
    response_model=ProductoCategoria,
    status_code=status.HTTP_201_CREATED,
)
def post_producto_categoria(payload: ProductoCategoriaCreate, session: Session = Depends(get_session)) -> ProductoCategoria:
    return crear_relacion(payload, session)

@router.delete("/{producto_id}/{categoria_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_producto_categoria(producto_id: int, categoria_id: int, session: Session = Depends(get_session)) -> None:
    eliminar_relacion(producto_id, categoria_id, session)
