from pydantic import BaseModel, Field

class IngredienteBase(BaseModel):
    nombre: str = Field(min_length=2, max_length=80)
    descripcion: str = Field(min_length=2, max_length=250)
    imagen_url: str | None = None

class IngredienteCreate(IngredienteBase):
    pass

class IngredienteUpdate(IngredienteBase):
    pass

class Ingrediente(IngredienteBase):
    id: int
