from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.categoria.router import router as categoria_router
from app.producto.router import router as producto_router
from app.producto_categoria.router import router as producto_categoria_router


app = FastAPI(title="API Productos y Categorías")

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


@app.get("/")
def healthcheck() -> dict[str, str]:
    return {"message": "API funcionando correctamente"}
