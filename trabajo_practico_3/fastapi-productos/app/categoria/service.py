from fastapi import HTTPException

from app.categoria.model import CategoriaModel
from app.categoria.schema import CategoriaCreate, CategoriaUpdate
from app.core.database import categorias_db, siguiente_id_categorias


def listar_categorias() -> list[CategoriaModel]:
    return categorias_db


def obtener_categoria(categoria_id: int) -> CategoriaModel:
    categoria = next((cat for cat in categorias_db if cat.id == categoria_id), None)
    if categoria is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return categoria


def crear_categoria(payload: CategoriaCreate) -> CategoriaModel:
    nueva_categoria = CategoriaModel(
        id=siguiente_id_categorias(),
        nombre=payload.nombre,
        descripcion=payload.descripcion,
    )
    categorias_db.append(nueva_categoria)
    return nueva_categoria


def actualizar_categoria(categoria_id: int, payload: CategoriaUpdate) -> CategoriaModel:
    categoria = obtener_categoria(categoria_id)
    categoria.nombre = payload.nombre
    categoria.descripcion = payload.descripcion
    return categoria


def eliminar_categoria(categoria_id: int) -> None:
    categoria = obtener_categoria(categoria_id)
    categorias_db.remove(categoria)
