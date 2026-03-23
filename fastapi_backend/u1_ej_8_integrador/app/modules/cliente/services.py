from typing import List, Optional

from .schemas import ClienteCreate, ClienteRead


def _calcular_riesgo_credito(limite_credito: float, saldo_pendiente: float) -> str:
    porcentaje = saldo_pendiente / limite_credito
    if porcentaje >= 0.8:
        return "alto"
    if porcentaje >= 0.5:
        return "medio"
    return "bajo"


def _email_duplicado(email: str, excluir_id: Optional[int] = None) -> bool:
    for cliente in db_clientes:
        if cliente.email == email and cliente.id != excluir_id:
            return True
    return False


db_clientes: List[ClienteRead] = [
    ClienteRead(
        id=1,
        nombre="Lucia Fernandez",
        email="lucia@email.com",
        ciudad="Cordoba",
        edad=30,
        limite_credito=150000,
        saldo_pendiente=12000,
        activo=True,
        riesgo_credito="bajo",
    ),
    ClienteRead(
        id=2,
        nombre="Martin Lopez",
        email="martin@email.com",
        ciudad="Rosario",
        edad=41,
        limite_credito=80000,
        saldo_pendiente=55000,
        activo=True,
        riesgo_credito="medio",
    ),
]
id_counter = 3


def crear(data: ClienteCreate) -> ClienteRead:
    global id_counter

    if _email_duplicado(data.email):
        raise ValueError("Ya existe un cliente con ese email")

    riesgo_credito = _calcular_riesgo_credito(data.limite_credito, data.saldo_pendiente)
    nuevo = ClienteRead(id=id_counter, riesgo_credito=riesgo_credito, **data.model_dump())

    db_clientes.append(nuevo)
    id_counter += 1
    return nuevo


def obtener_todos(
    skip: int = 0,
    limit: int = 10,
    activo: Optional[bool] = None,
    ciudad: Optional[str] = None,
    edad_min: Optional[int] = None,
    edad_max: Optional[int] = None,
    riesgo: Optional[str] = None,
    buscar: Optional[str] = None,
) -> List[ClienteRead]:
    if edad_min is not None and edad_max is not None and edad_min > edad_max:
        raise ValueError("edad_min no puede ser mayor que edad_max")

    if riesgo is not None and riesgo not in {"bajo", "medio", "alto"}:
        raise ValueError("El riesgo debe ser: bajo, medio o alto")

    resultados = db_clientes

    if activo is not None:
        resultados = [c for c in resultados if c.activo == activo]

    if ciudad:
        ciudad_normalizada = ciudad.strip().lower()
        resultados = [c for c in resultados if c.ciudad.lower() == ciudad_normalizada]

    if edad_min is not None:
        resultados = [c for c in resultados if c.edad >= edad_min]

    if edad_max is not None:
        resultados = [c for c in resultados if c.edad <= edad_max]

    if riesgo is not None:
        resultados = [c for c in resultados if c.riesgo_credito == riesgo]

    if buscar:
        termino = buscar.strip().lower()
        resultados = [
            c
            for c in resultados
            if termino in c.nombre.lower() or termino in c.email.lower()
        ]

    return resultados[skip : skip + limit]


def obtener_por_id(id: int) -> Optional[ClienteRead]:
    for cliente in db_clientes:
        if cliente.id == id:
            return cliente
    return None


def actualizar_total(id: int, data: ClienteCreate) -> Optional[ClienteRead]:
    if _email_duplicado(data.email, excluir_id=id):
        raise ValueError("Ya existe un cliente con ese email")

    for index, cliente in enumerate(db_clientes):
        if cliente.id == id:
            riesgo_credito = _calcular_riesgo_credito(
                data.limite_credito, data.saldo_pendiente
            )
            actualizado = ClienteRead(
                id=id, riesgo_credito=riesgo_credito, **data.model_dump()
            )
            db_clientes[index] = actualizado
            return actualizado
    return None


def desactivar(id: int) -> Optional[ClienteRead]:
    for index, cliente in enumerate(db_clientes):
        if cliente.id == id:
            if cliente.saldo_pendiente > 0:
                raise RuntimeError(
                    "No se puede desactivar un cliente con saldo pendiente"
                )
            cliente_dict = cliente.model_dump()
            cliente_dict["activo"] = False
            actualizado = ClienteRead(**cliente_dict)
            db_clientes[index] = actualizado
            return actualizado
    return None


def registrar_pago(id: int, monto: float) -> Optional[ClienteRead]:
    if monto <= 0:
        raise ValueError("El monto debe ser mayor que 0")

    for index, cliente in enumerate(db_clientes):
        if cliente.id == id:
            if monto > cliente.saldo_pendiente:
                raise ValueError("El monto excede el saldo pendiente")

            cliente_dict = cliente.model_dump()
            cliente_dict["saldo_pendiente"] = round(
                cliente.saldo_pendiente - monto, 2
            )
            cliente_dict["riesgo_credito"] = _calcular_riesgo_credito(
                cliente.limite_credito, cliente_dict["saldo_pendiente"]
            )

            actualizado = ClienteRead(**cliente_dict)
            db_clientes[index] = actualizado
            return actualizado
    return None


def obtener_estado_credito(id: int) -> Optional[dict]:
    cliente = obtener_por_id(id)
    if not cliente:
        return None

    return {
        "saldo_pendiente": cliente.saldo_pendiente,
        "limite_credito": cliente.limite_credito,
        "riesgo_credito": cliente.riesgo_credito,
    }
