from sqlmodel import SQLModel


# ── Input ──────────────────────────────────────────────────────────────────────

class ProductCreate(SQLModel):
    name: str
    price: float


# ── Output ─────────────────────────────────────────────────────────────────────

class ProductRead(SQLModel):
    id: int
    name: str
    price: float
