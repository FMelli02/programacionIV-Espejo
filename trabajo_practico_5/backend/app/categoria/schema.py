from pydantic import BaseModel, Field


class CategoriaBase(BaseModel):
    nombre: str = Field(min_length=2, max_length=80)
    descripcion: str = Field(min_length=2, max_length=250)


class CategoriaCreate(CategoriaBase):
    pass


class CategoriaUpdate(CategoriaBase):
    pass


class Categoria(CategoriaBase):
    id: int
