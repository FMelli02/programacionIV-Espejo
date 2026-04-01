from typing import List, Optional

from sqlalchemy import or_
from sqlmodel import Session, select

from .models import Cliente
from .schemas import ClienteCreate


def _calcular_riesgo_credito(limite_credito: float, saldo_pendiente: float) -> str:
    porcentaje = saldo_pendiente / limite_credito
    if porcentaje >= 0.8:
        return "alto"
    if porcentaje >= 0.5:
        return "medio"
    return "bajo"


def _email_duplicado(session: Session, email: str, excluir_id: Optional[int] = None) -> bool:
    statement = select(Cliente).where(Cliente.email == email)
    if excluir_id is not None:
        statement = statement.where(Cliente.id != excluir_id)
    return session.exec(statement).first() is not None


def crear(session: Session, data: ClienteCreate) -> Cliente:
    if _email_duplicado(session, data.email):
        raise ValueError("Ya existe un cliente con ese email")

    riesgo_credito = _calcular_riesgo_credito(data.limite_credito, data.saldo_pendiente)
    nuevo = Cliente(riesgo_credito=riesgo_credito, **data.model_dump())
    session.add(nuevo)
    session.commit()
    session.refresh(nuevo)
    return nuevo


def obtener_todos(
    session: Session,
    skip: int = 0,
    limit: int = 10,
    activo: Optional[bool] = None,
    ciudad: Optional[str] = None,
    edad_min: Optional[int] = None,
    edad_max: Optional[int] = None,
    riesgo: Optional[str] = None,
    buscar: Optional[str] = None,
) -> List[Cliente]:
    if edad_min is not None and edad_max is not None and edad_min > edad_max:
        raise ValueError("edad_min no puede ser mayor que edad_max")

    if riesgo is not None and riesgo not in {"bajo", "medio", "alto"}:
        raise ValueError("El riesgo debe ser: bajo, medio o alto")

    statement = select(Cliente)

    if activo is not None:
        statement = statement.where(Cliente.activo == activo)

    if ciudad:
        ciudad_normalizada = ciudad.strip().lower()
        statement = statement.where(Cliente.ciudad.ilike(ciudad_normalizada))

    if edad_min is not None:
        statement = statement.where(Cliente.edad >= edad_min)

    if edad_max is not None:
        statement = statement.where(Cliente.edad <= edad_max)

    if riesgo is not None:
        statement = statement.where(Cliente.riesgo_credito == riesgo)

    if buscar:
        termino = f"%{buscar.strip().lower()}%"
        statement = statement.where(
            or_(Cliente.nombre.ilike(termino), Cliente.email.ilike(termino))
        )

    statement = statement.offset(skip).limit(limit)
    return list(session.exec(statement).all())


def obtener_por_id(session: Session, id: int) -> Optional[Cliente]:
    return session.get(Cliente, id)


def actualizar_total(session: Session, id: int, data: ClienteCreate) -> Optional[Cliente]:
    if _email_duplicado(session, data.email, excluir_id=id):
        raise ValueError("Ya existe un cliente con ese email")

    cliente = session.get(Cliente, id)
    if not cliente:
        return None

    riesgo_credito = _calcular_riesgo_credito(data.limite_credito, data.saldo_pendiente)
    payload = data.model_dump()
    payload["riesgo_credito"] = riesgo_credito

    for field, value in payload.items():
        setattr(cliente, field, value)

    session.add(cliente)
    session.commit()
    session.refresh(cliente)
    return cliente


def desactivar(session: Session, id: int) -> Optional[Cliente]:
    cliente = session.get(Cliente, id)
    if not cliente:
        return None

    if cliente.saldo_pendiente > 0:
        raise RuntimeError("No se puede desactivar un cliente con saldo pendiente")

    cliente.activo = False
    session.add(cliente)
    session.commit()
    session.refresh(cliente)
    return cliente


def registrar_pago(session: Session, id: int, monto: float) -> Optional[Cliente]:
    if monto <= 0:
        raise ValueError("El monto debe ser mayor que 0")

    cliente = session.get(Cliente, id)
    if not cliente:
        return None

    if monto > cliente.saldo_pendiente:
        raise ValueError("El monto excede el saldo pendiente")

    cliente.saldo_pendiente = round(cliente.saldo_pendiente - monto, 2)
    cliente.riesgo_credito = _calcular_riesgo_credito(
        cliente.limite_credito, cliente.saldo_pendiente
    )

    session.add(cliente)
    session.commit()
    session.refresh(cliente)
    return cliente


def obtener_estado_credito(session: Session, id: int) -> Optional[dict]:
    cliente = obtener_por_id(session, id)
    if not cliente:
        return None

    return {
        "saldo_pendiente": cliente.saldo_pendiente,
        "limite_credito": cliente.limite_credito,
        "riesgo_credito": cliente.riesgo_credito,
    }
