from app.categoria.model import CategoriaModel
from app.producto.model import ProductoModel
from app.producto_categoria.model import ProductoCategoriaModel


categorias_db: list[CategoriaModel] = [
    CategoriaModel(id=1, nombre="Pizzas", descripcion="Pizzas artesanales con masa fresca"),
    CategoriaModel(id=2, nombre="Hamburguesas", descripcion="Hamburguesas gourmet"),
]

productos_db: list[ProductoModel] = [
    ProductoModel(
        id=1,
        nombre="Muzzarella",
        descripcion="Pizza clásica",
        preciobase="8500",
        imagenurl=["https://imagenes-ejemplo.com/muzza.jpg"],
        disponible=True,
    )
]

producto_categorias_db: list[ProductoCategoriaModel] = [
    ProductoCategoriaModel(productoid=1, categoriaid=1)
]


def siguiente_id_categorias() -> int:
    if not categorias_db:
        return 1
    return max(cat.id for cat in categorias_db) + 1


def siguiente_id_productos() -> int:
    if not productos_db:
        return 1
    return max(prod.id for prod in productos_db) + 1
