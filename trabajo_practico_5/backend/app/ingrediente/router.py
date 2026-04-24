from fastapi import APIRouter, status, Depends
from sqlmodel import Session
from app.core.database import get_session
from app.ingrediente.model import Ingrediente
from app.ingrediente.schema import IngredienteCreate, IngredienteUpdate
from app.ingrediente.service import (
    actualizar_ingrediente,
    crear_ingrediente,
    eliminar_ingrediente,
    listar_ingredientes,
)

router = APIRouter(prefix="/ingredientes", tags=["Ingredientes"])

@router.get("", response_model=list[Ingrediente])
def get_ingredientes(session: Session = Depends(get_session)) -> list[Ingrediente]:
    return listar_ingredientes(session)

@router.post("", response_model=Ingrediente, status_code=status.HTTP_201_CREATED)
def post_ingrediente(payload: IngredienteCreate, session: Session = Depends(get_session)) -> Ingrediente:
    return crear_ingrediente(payload, session)

@router.put("/{ingrediente_id}", response_model=Ingrediente)
def put_ingrediente(ingrediente_id: int, payload: IngredienteUpdate, session: Session = Depends(get_session)) -> Ingrediente:
    return actualizar_ingrediente(ingrediente_id, payload, session)

@router.delete("/{ingrediente_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ingrediente(ingrediente_id: int, session: Session = Depends(get_session)) -> None:
    eliminar_ingrediente(ingrediente_id, session)
