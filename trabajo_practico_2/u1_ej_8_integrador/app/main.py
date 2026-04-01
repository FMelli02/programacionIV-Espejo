from fastapi import FastAPI
from sqlmodel import Session

from app.db import create_db_and_tables, engine
from app.modules.categoria import models as categoria_models  # noqa: F401
from app.modules.cliente import models as cliente_models  # noqa: F401
from app.modules.producto import models as producto_models  # noqa: F401
from app.modules.producto.routers import router as producto_router
from app.modules.categoria.routers import router as categoria_router
from app.modules.cliente.routers import router as cliente_router
from app.seed import seed_initial_data

def create_app() -> FastAPI:
    app = FastAPI(
        title="API Integradora - Unidad 1",
        description="Conceptos: Path, Query, Body, Pydantic, Errores.",
        version="1.0.0"
    )

    @app.on_event("startup")
    def on_startup() -> None:
        create_db_and_tables()
        with Session(engine) as session:
            seed_initial_data(session)
    
    app.include_router(producto_router)
    app.include_router(categoria_router)
    app.include_router(cliente_router)
    
    return app

app = create_app()
