from fastapi import FastAPI

from app.database import create_db_and_tables
from app.routers import products_router, orders_router

app = FastAPI(title="Sistema de Órdenes", version="1.0.0")


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


app.include_router(products_router)
app.include_router(orders_router)
