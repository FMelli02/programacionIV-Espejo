## TP2 - Migracion a PostgreSQL

### Opcion recomendada: Docker (sin instalar PostgreSQL local)

Levantar todo el stack (PostgreSQL + API):

```powershell
docker compose up --build
```

Esto hace automaticamente:

1. Levanta PostgreSQL.
2. Ejecuta `alembic upgrade head`.
3. Inicia la API en `http://127.0.0.1:8000`.

### 1. Instalar dependencias

```powershell
python -m pip install -r requirements.txt
```

### 2. Configurar base de datos

El proyecto usa la variable `DATABASE_URL`.

Ejemplo:

```env
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/gestor_productos
```

Referencia de ejemplo disponible en `.env.example`.

### 3. Ejecutar migraciones Alembic

```powershell
python -m alembic upgrade head
```

### 4. Levantar la API

```powershell
cd u1_ej_8_integrador
python -m fastapi dev app/main.py
```

### 5. Probar endpoints

Swagger UI:

- http://127.0.0.1:8000/docs

REST Client:

- `u1_ej_8_integrador/tests/test_api.http`

Checklist de verificacion manual en Swagger:

- `u1_ej_8_integrador/tests/swagger_checklist.md`

### Entregables para el zip

1. `u1_ej_8_integrador/tests/test_api.http`
2. `u1_ej_8_integrador/tests/RESTCLIENT_EVIDENCIA.md`
3. `u1_ej_8_integrador/tests/json/categoria_create.json`
4. `u1_ej_8_integrador/tests/json/producto_create.json`
5. `u1_ej_8_integrador/tests/json/cliente_create.json`
6. `u1_ej_8_integrador/tests/json/filtros_clientes.json`
7. `u1_ej_8_integrador/tests/swagger_checklist.md`
8. Codigo fuente con SQLModel + Alembic + Docker.
