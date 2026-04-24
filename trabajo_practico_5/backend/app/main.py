from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.database import create_db_and_tables
from app.categoria.router import router as categoria_router
from app.producto.router import router as producto_router
from app.producto_categoria.router import router as producto_categoria_router
from app.ingrediente.router import router as ingrediente_router
from app.ventas.router import router as ventas_router
import app.ventas.model  # Import models so SQLModel registers them
import app.ingrediente.model

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(title="API Productos y Categorías", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(categoria_router)
app.include_router(producto_router)
app.include_router(producto_categoria_router)
app.include_router(ingrediente_router)
app.include_router(ventas_router)


@app.get("/")
def healthcheck() -> dict[str, str]:
    return {"message": "API funcionando correctamente"}
