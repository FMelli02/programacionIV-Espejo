from fastapi import APIRouter, status, Depends
from sqlmodel import Session
from app.core.database import get_session
from app.ventas.schema import PedidoResponse, PedidoCreate, PedidoUpdate
from app.ventas.service import (
    actualizar_pedido,
    crear_pedido,
    eliminar_pedido,
    listar_pedidos,
)

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])

@router.get("", response_model=list[PedidoResponse])
def get_pedidos(session: Session = Depends(get_session)):
    return listar_pedidos(session)

@router.post("", response_model=PedidoResponse, status_code=status.HTTP_201_CREATED)
def post_pedido(payload: PedidoCreate, session: Session = Depends(get_session)):
    return crear_pedido(payload, session)

@router.put("/{pedido_id}", response_model=PedidoResponse)
def put_pedido(pedido_id: int, payload: PedidoUpdate, session: Session = Depends(get_session)):
    return actualizar_pedido(pedido_id, payload, session)

@router.delete("/{pedido_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pedido(pedido_id: int, session: Session = Depends(get_session)):
    eliminar_pedido(pedido_id, session)
