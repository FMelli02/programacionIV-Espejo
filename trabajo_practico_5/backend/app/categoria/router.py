from fastapi import APIRouter, status, Depends
from sqlmodel import Session
from app.core.database import get_session
from app.categoria.model import Categoria
from app.categoria.schema import CategoriaCreate, CategoriaUpdate
from app.categoria.service import (
    actualizar_categoria,
    crear_categoria,
    eliminar_categoria,
    listar_categorias,
)

router = APIRouter(prefix="/categorias", tags=["Categorias"])

@router.get("", response_model=list[Categoria])
def get_categorias(session: Session = Depends(get_session)) -> list[Categoria]:
    return listar_categorias(session)

@router.post("", response_model=Categoria, status_code=status.HTTP_201_CREATED)
def post_categoria(payload: CategoriaCreate, session: Session = Depends(get_session)) -> Categoria:
    return crear_categoria(payload, session)

@router.put("/{categoria_id}", response_model=Categoria)
def put_categoria(categoria_id: int, payload: CategoriaUpdate, session: Session = Depends(get_session)) -> Categoria:
    return actualizar_categoria(categoria_id, payload, session)

@router.delete("/{categoria_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_categoria(categoria_id: int, session: Session = Depends(get_session)) -> None:
    eliminar_categoria(categoria_id, session)
