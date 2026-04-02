from pydantic import BaseModel


class ProductoCategoriaBase(BaseModel):
    productoid: int
    categoriaid: int


class ProductoCategoriaCreate(ProductoCategoriaBase):
    pass


class ProductoCategoria(ProductoCategoriaBase):
    pass
