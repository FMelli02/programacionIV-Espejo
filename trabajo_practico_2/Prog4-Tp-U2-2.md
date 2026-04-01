# PROGRAMACIÓN III

# Trabajo Práctico - Migración a PostgreSQL

## OBJETIVO GENERAL

Migrar el "Gestor de Productos" de almacenamiento en memoria a PostgreSQL utilizando SQLModel, manteniendo todas las validaciones existentes y demostrando comprensión de la arquitectura modular FastAPI con persistencia de datos.

**MARCO TEÓRICO**


| Concepto | Aplicación en el proyecto |
| --- | --- |
| FastAPI | Framework moderno de Python para crear APIs RESTful con<br>validación automática de datos y documentación interactiva. |
| SQLModel | Biblioteca que combina SQLAlchemy ORM y Pydantic,<br>permitiendo definir modelos de datos que sirven tanto para<br>base de datos como para validación. |
| Pydantic | Biblioteca de validación de datos que define schemas para<br>request/response bodies con validación automática de tipos y<br>constraints. |
| Arquitectura en capas | Patrón de diseño que separa responsabilidades en capas:<br>Router (HTTP), Service (lógica de negocio), Repository (acceso<br>a datos), Model (entidades). |
| PostgreSQL | Sistema de gestión de base de datos relacional de código<br>abierto, que reemplaza el almacenamiento en memoria con<br>persistencia real. |
| Alembic | Herramienta de migraciones que gestiona cambios en el<br>esquema de la base de datos de forma versionada y reversible. |


### CASO PRÁCTICO

**Dado el el Trabajo Práctico de la unidad 1:**

**a) Migrar el proyecto y añadir PostgreSQL**

**b) Probar endPoints (Postman/restClient)**

**c) Agregar al archivo .zip los json de prueba**

**d) Verificar en Swagger UI**

- Acceder a http://localhost:8000/docs

- Probar cada endpoint interactivamente

- Verificar schemas en la documentación


## CONCLUSIONES ESPERADAS

### Al finalizar el trabajo práctico, el estudiante debe demostrar:

**·Arquitectura** **modular**: Separación clara entre capas (Router → Service →Schema→ Model)

**·Persistencia** **con** **SQLModel**: Uso correcto de ORM,relaciones y sesiones de base de datos

**·** **Validaciones** **roobustas**: Validaciones a nivel de Pydantic (schemas) y reglas de negocio (service)

**·Manejo** **de** **errores**: Respuestas HTTP apropiadas para casos de éxito y error

**·Buenas** **prácticas:** Código modular, reutilizable, siguiendo principios de Clean Architecture

### Documentación oficial:

·FastAPI: https://fastapi.tiangolo.com/

SQLModel:https://sqlmodel.tiangolo.com/

·Alembic: https://alembic.sqlalchemy.org/

·Pydantic: https://docs.pydantic.dev/

<!-- 2 -->

<!-- PROGRAMACIÓN IV -->

