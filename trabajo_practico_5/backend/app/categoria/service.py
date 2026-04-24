from sqlmodel import Session, select
from fastapi import HTTPException
from app.categoria.model import Categoria
from app.categoria.schema import CategoriaCreate, CategoriaUpdate
from datetime import datetime, timezone

def listar_categorias(session: Session) -> list[Categoria]:
    return session.exec(select(Categoria).where(Categoria.deleted_at == None)).all()

def obtener_categoria(categoria_id: int, session: Session) -> Categoria:
    categoria = session.get(Categoria, categoria_id)
    if not categoria or categoria.deleted_at is not None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return categoria

def crear_categoria(payload: CategoriaCreate, session: Session) -> Categoria:
    categoria = Categoria(**payload.model_dump())
    session.add(categoria)
    session.commit()
    session.refresh(categoria)
    return categoria

def actualizar_categoria(categoria_id: int, payload: CategoriaUpdate, session: Session) -> Categoria:
    categoria = obtener_categoria(categoria_id, session)
    categoria_data = payload.model_dump(exclude_unset=True)
    for key, value in categoria_data.items():
        setattr(categoria, key, value)
    categoria.updated_at = datetime.now(timezone.utc)
    session.add(categoria)
    session.commit()
    session.refresh(categoria)
    return categoria

def eliminar_categoria(categoria_id: int, session: Session) -> None:
    categoria = obtener_categoria(categoria_id, session)
    # Soft delete
    categoria.deleted_at = datetime.now(timezone.utc)
    session.add(categoria)
    session.commit()
