# Sistema de Órdenes - Práctica FastAPI + SQLModel

Esta es una API RESTful desarrollada con **FastAPI**, **SQLModel** y **Pydantic** para gestionar productos y órdenes, aplicando el patrón Unit of Work y manteniendo una separación en capas (Modelos y Schemas separadamente).

## Requisitos

- Python 3.10 o superior.

## Instalación y Configuración

1. Crear un entorno virtual (opcional pero recomendado):
   ```bash
   python -m venv venv
   # En Windows:
   venv\Scripts\activate
   # En Linux/Mac:
   source venv/bin/activate
   ```

2. Instalar las dependencias listadas en `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

## Ejecución del Servidor

Para levantar la aplicación en modo desarrollo, ejecutá el siguiente comando:

```bash
uvicorn app.main:app --reload --reload-dir app --port 8000
```
> *(Si `uvicorn` no te es reconocido como comando, probá ejecutándolo a través del módulo de python con `python -m uvicorn app.main:app --reload --reload-dir app --port 8000`)*

El servidor estará funcionando en http://127.0.0.1:8000. 
Al iniciarse, la aplicación creará automáticamente el archivo de base de datos local `ordenes.db`.

## Documentación Interactiva

FastAPI provee la documentación generada automáticamente (Swagger UI) para probar todos los endpoints de tu API.
Una vez que el servidor esté corriendo, podés ingresar a:

👉 **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**

## Consideraciones del Desarrollo

- **Base de Datos Local**: Este desarrollo utiliza un archivo *SQLite* local llamado `ordenes.db` por comodidad para la entrega. No es necesario configurar variables de entorno (no hay archivo `.env`).
- **Imports Circulares**: Se agrupó el modelo de datos en `app.models.__init__.py` para evadir conflictos y circularidad en tiempo de ejecución propios del parseo de relaciones de SQLModel.
- **Unit of Work**: Todo proceso de creación de órdenes ocurre garantizando transaccionalidad. Si se busca comprar un producto inexistente, se cancela y no impacta la base de datos.
