from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlmodel import Session

from app.db import get_session

from . import schemas, services

router = APIRouter(prefix="/clientes", tags=["Clientes"])


@router.post("/", response_model=schemas.ClienteRead, status_code=status.HTTP_201_CREATED)
def alta_cliente(
    cliente: schemas.ClienteCreate, session: Session = Depends(get_session)
):
    try:
        return services.crear(session, cliente)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))


@router.get("/", response_model=List[schemas.ClienteRead], status_code=status.HTTP_200_OK)
def listar_clientes(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=50),
    activo: Optional[bool] = None,
    ciudad: Optional[str] = None,
    edad_min: Optional[int] = Query(None, ge=18, le=99),
    edad_max: Optional[int] = Query(None, ge=18, le=99),
    riesgo: Optional[str] = None,
    buscar: Optional[str] = None,
    session: Session = Depends(get_session),
):
    try:
        return services.obtener_todos(
            session=session,
            skip=skip,
            limit=limit,
            activo=activo,
            ciudad=ciudad,
            edad_min=edad_min,
            edad_max=edad_max,
            riesgo=riesgo,
            buscar=buscar,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.get("/{id}", response_model=schemas.ClienteRead, status_code=status.HTTP_200_OK)
def detalle_cliente(id: int = Path(..., gt=0), session: Session = Depends(get_session)):
    cliente = services.obtener_por_id(session, id)
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado"
        )
    return cliente


@router.put("/{id}", response_model=schemas.ClienteRead, status_code=status.HTTP_200_OK)
def actualizar_cliente(
    cliente: schemas.ClienteCreate,
    id: int = Path(..., gt=0),
    session: Session = Depends(get_session),
):
    try:
        actualizado = services.actualizar_total(session, id, cliente)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))

    if not actualizado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado"
        )
    return actualizado


@router.put(
    "/{id}/desactivar",
    response_model=schemas.ClienteRead,
    status_code=status.HTTP_200_OK,
)
def baja_logica_cliente(
    id: int = Path(..., gt=0), session: Session = Depends(get_session)
):
    try:
        desactivado = services.desactivar(session, id)
    except RuntimeError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))

    if not desactivado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado"
        )
    return desactivado


@router.put(
    "/{id}/pagar",
    response_model=schemas.ClienteSaldoResponse,
    status_code=status.HTTP_200_OK,
)
def pagar_saldo(
    id: int = Path(..., gt=0),
    monto: float = Query(..., gt=0),
    session: Session = Depends(get_session),
):
    try:
        cliente_actualizado = services.registrar_pago(session=session, id=id, monto=monto)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))

    if not cliente_actualizado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado"
        )

    return {
        "saldo_pendiente": cliente_actualizado.saldo_pendiente,
        "limite_credito": cliente_actualizado.limite_credito,
        "riesgo_credito": cliente_actualizado.riesgo_credito,
    }


@router.get(
    "/{id}/credito",
    response_model=schemas.ClienteSaldoResponse,
    status_code=status.HTTP_200_OK,
)
def estado_credito(id: int = Path(..., gt=0), session: Session = Depends(get_session)):
    estado = services.obtener_estado_credito(session, id)
    if not estado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado"
        )
    return estado
