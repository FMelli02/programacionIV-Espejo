from sqlmodel import Session, select
from fastapi import HTTPException
from app.ingrediente.model import Ingrediente
from app.ingrediente.schema import IngredienteCreate, IngredienteUpdate
from datetime import datetime, timezone

def listar_ingredientes(session: Session) -> list[Ingrediente]:
    return session.exec(select(Ingrediente).where(Ingrediente.deleted_at == None)).all()

def obtener_ingrediente(ingrediente_id: int, session: Session) -> Ingrediente:
    ingrediente = session.get(Ingrediente, ingrediente_id)
    if not ingrediente or ingrediente.deleted_at is not None:
        raise HTTPException(status_code=404, detail="Ingrediente no encontrado")
    return ingrediente

def crear_ingrediente(payload: IngredienteCreate, session: Session) -> Ingrediente:
    ingrediente = Ingrediente(**payload.model_dump())
    session.add(ingrediente)
    session.commit()
    session.refresh(ingrediente)
    return ingrediente

def actualizar_ingrediente(ingrediente_id: int, payload: IngredienteUpdate, session: Session) -> Ingrediente:
    ingrediente = obtener_ingrediente(ingrediente_id, session)
    ingrediente_data = payload.model_dump(exclude_unset=True)
    for key, value in ingrediente_data.items():
        setattr(ingrediente, key, value)
    ingrediente.updated_at = datetime.now(timezone.utc)
    session.add(ingrediente)
    session.commit()
    session.refresh(ingrediente)
    return ingrediente

def eliminar_ingrediente(ingrediente_id: int, session: Session) -> None:
    ingrediente = obtener_ingrediente(ingrediente_id, session)
    ingrediente.deleted_at = datetime.now(timezone.utc)
    session.add(ingrediente)
    session.commit()
