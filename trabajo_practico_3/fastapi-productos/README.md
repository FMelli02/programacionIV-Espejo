# fastapi-productos

Backend del TP Integrador (Programación IV).

## Requisitos

- Python 3.10+

## Instalación

```bash
python -m venv .venv
```

### Activar entorno

- **Windows**

```bash
.venv\Scripts\activate
```

- **macOS/Linux**

```bash
source .venv/bin/activate
```

### Instalar dependencias

```bash
pip install -r requirements.txt
```

## Ejecutar servidor

```bash
python -m uvicorn app.main:app --reload
```

Documentación automática: http://localhost:8000/docs

## Pruebas REST Client

El archivo `rest-client.http` contiene ejemplos para:

- Categorías
- Productos
- Relación Producto-Categoría
