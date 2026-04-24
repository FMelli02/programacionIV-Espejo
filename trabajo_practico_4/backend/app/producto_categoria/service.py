from sqlmodel import Session, select
from fastapi import HTTPException
from app.producto_categoria.model import ProductoCategoria
from app.producto_categoria.schema import ProductoCategoriaCreate

def listar_relaciones(session: Session) -> list[ProductoCategoria]:
    return session.exec(select(ProductoCategoria)).all()

def crear_relacion(payload: ProductoCategoriaCreate, session: Session) -> ProductoCategoria:
    # Check if exists
    relacion = session.get(ProductoCategoria, (payload.producto_id, payload.categoria_id))
    if relacion:
        raise HTTPException(status_code=400, detail="La relación ya existe")
    
    nueva_relacion = ProductoCategoria(**payload.model_dump())
    session.add(nueva_relacion)
    session.commit()
    session.refresh(nueva_relacion)
    return nueva_relacion

def eliminar_relacion(producto_id: int, categoria_id: int, session: Session) -> None:
    relacion = session.get(ProductoCategoria, (producto_id, categoria_id))
    if not relacion:
        raise HTTPException(status_code=404, detail="Relación no encontrada")
    session.delete(relacion)
    session.commit()
