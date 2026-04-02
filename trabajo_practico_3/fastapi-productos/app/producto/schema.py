from pydantic import BaseModel, Field


class ProductoBase(BaseModel):
    nombre: str = Field(min_length=2, max_length=120)
    descripcion: str = Field(min_length=2, max_length=250)
    preciobase: str = Field(min_length=1, max_length=20)
    imagenurl: list[str] = Field(default_factory=list)
    disponible: bool = True


class ProductoCreate(ProductoBase):
    pass


class ProductoUpdate(ProductoBase):
    pass


class Producto(ProductoBase):
    id: int
