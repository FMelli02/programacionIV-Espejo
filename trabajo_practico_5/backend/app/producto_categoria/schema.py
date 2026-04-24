from pydantic import BaseModel

class ProductoCategoriaBase(BaseModel):
    producto_id: int
    categoria_id: int
    es_principal: bool = False

class ProductoCategoriaCreate(ProductoCategoriaBase):
    pass

class ProductoCategoria(ProductoCategoriaBase):
    pass
