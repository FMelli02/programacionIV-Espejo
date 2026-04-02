from fastapi import APIRouter, status

from app.categoria.schema import Categoria, CategoriaCreate, CategoriaUpdate
from app.categoria.service import (
    actualizar_categoria,
    crear_categoria,
    eliminar_categoria,
    listar_categorias,
)


router = APIRouter(prefix="/categorias", tags=["Categorias"])


@router.get("", response_model=list[Categoria])
def get_categorias() -> list[Categoria]:
    return listar_categorias()


@router.post("", response_model=Categoria, status_code=status.HTTP_201_CREATED)
def post_categoria(payload: CategoriaCreate) -> Categoria:
    return crear_categoria(payload)


@router.put("/{categoria_id}", response_model=Categoria)
def put_categoria(categoria_id: int, payload: CategoriaUpdate) -> Categoria:
    return actualizar_categoria(categoria_id, payload)


@router.delete("/{categoria_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_categoria(categoria_id: int) -> None:
    eliminar_categoria(categoria_id)
