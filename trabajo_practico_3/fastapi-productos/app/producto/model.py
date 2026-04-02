from dataclasses import dataclass


@dataclass
class ProductoModel:
    id: int
    nombre: str
    descripcion: str
    preciobase: str
    imagenurl: list[str]
    disponible: bool
