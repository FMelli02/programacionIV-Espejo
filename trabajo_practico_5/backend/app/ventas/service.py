from sqlmodel import Session, select
from fastapi import HTTPException
from app.ventas.model import Pedido, DetallePedido
from app.ventas.schema import PedidoCreate, PedidoUpdate
from datetime import datetime, timezone
from decimal import Decimal

def listar_pedidos(session: Session) -> list[Pedido]:
    return session.exec(select(Pedido).where(Pedido.deleted_at == None)).all()

def obtener_pedido(pedido_id: int, session: Session) -> Pedido:
    pedido = session.get(Pedido, pedido_id)
    if not pedido or pedido.deleted_at is not None:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return pedido

def crear_pedido(payload: PedidoCreate, session: Session) -> Pedido:
    subtotal = Decimal("0.00")
    for det in payload.detalles:
        subtotal += det.precio_snapshot * det.cantidad
    
    total = subtotal - payload.descuento + payload.costo_envio
    
    pedido = Pedido(
        usuario_id=payload.usuario_id,
        direccion_id=payload.direccion_id,
        estado_codigo=payload.estado_codigo,
        forma_pago_codigo=payload.forma_pago_codigo,
        subtotal=subtotal,
        descuento=payload.descuento,
        costo_envio=payload.costo_envio,
        total=total,
        notas=payload.notas
    )
    session.add(pedido)
    session.commit()
    session.refresh(pedido)
    
    for det in payload.detalles:
        # In a real scenario we fetch the producto to get `nombre_snapshot`
        # Here we hardcode "Producto Snapshot" for simplicity, or we can look it up.
        detalle = DetallePedido(
            pedido_id=pedido.id,
            producto_id=det.producto_id,
            cantidad=det.cantidad,
            nombre_snapshot=f"Producto {det.producto_id}",
            precio_snapshot=det.precio_snapshot,
            subtotal_snap=det.precio_snapshot * det.cantidad,
            personalizacion=det.personalizacion
        )
        session.add(detalle)
    
    session.commit()
    session.refresh(pedido)
    return pedido

def actualizar_pedido(pedido_id: int, payload: PedidoUpdate, session: Session) -> Pedido:
    pedido = obtener_pedido(pedido_id, session)
    if payload.estado_codigo:
        pedido.estado_codigo = payload.estado_codigo
    if payload.forma_pago_codigo:
        pedido.forma_pago_codigo = payload.forma_pago_codigo
    if payload.notas is not None:
        pedido.notas = payload.notas
        
    pedido.updated_at = datetime.now(timezone.utc)
    session.add(pedido)
    session.commit()
    session.refresh(pedido)
    return pedido

def eliminar_pedido(pedido_id: int, session: Session) -> None:
    pedido = obtener_pedido(pedido_id, session)
    pedido.deleted_at = datetime.now(timezone.utc)
    session.add(pedido)
    session.commit()
