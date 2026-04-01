from sqlmodel import Session, select

from app.modules.categoria.models import Categoria
from app.modules.cliente.models import Cliente


def _calcular_riesgo_credito(limite_credito: float, saldo_pendiente: float) -> str:
    porcentaje = saldo_pendiente / limite_credito
    if porcentaje >= 0.8:
        return "alto"
    if porcentaje >= 0.5:
        return "medio"
    return "bajo"


def seed_initial_data(session: Session) -> None:
    if session.exec(select(Categoria)).first() is None:
        session.add(
            Categoria(codigo="MUE-01", descripcion="Muebles de Oficina", activo=True)
        )
        session.add(Categoria(codigo="ELE-02", descripcion="Electrónica", activo=True))

    if session.exec(select(Cliente)).first() is None:
        session.add(
            Cliente(
                nombre="Lucia Fernandez",
                email="lucia@email.com",
                ciudad="Cordoba",
                edad=30,
                limite_credito=150000,
                saldo_pendiente=12000,
                activo=True,
                riesgo_credito=_calcular_riesgo_credito(150000, 12000),
            )
        )
        session.add(
            Cliente(
                nombre="Martin Lopez",
                email="martin@email.com",
                ciudad="Rosario",
                edad=41,
                limite_credito=80000,
                saldo_pendiente=55000,
                activo=True,
                riesgo_credito=_calcular_riesgo_credito(80000, 55000),
            )
        )

    session.commit()
