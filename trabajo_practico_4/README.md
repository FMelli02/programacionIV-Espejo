# 🛒 Food Store - Trabajo Práctico 4

Bienvenido al repositorio del **TP4** de Programación IV. Esta es una aplicación Full Stack para la gestión de una tienda de alimentos, construida con tecnologías modernas y una arquitectura escalable.

## 🚀 Tecnologías Utilizadas

### Backend

- **FastAPI**: Framework de alto rendimiento para construir APIs con Python.
- **SQLModel**: Librería que combina SQLAlchemy y Pydantic para la interacción con la base de datos.
- **PostgreSQL**: Base de datos relacional robusta.
- **Docker**: Contenerización de servicios para un despliegue consistente.

### Frontend

- **React**: Biblioteca para construir interfaces de usuario.
- **Vite**: Herramienta de construcción ultra rápida.
- **Tailwind CSS**: Framework de CSS para un diseño moderno y responsive.
- **TypeScript**: Tipado estático para un desarrollo más seguro.

---

## 🛠️ Requisitos Previos

Asegurate de tener instalado:

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Python 3.10+](https://www.python.org/downloads/) (para ejecución local)
- [Node.js 18+](https://nodejs.org/) (para ejecución local)

---

## 🐳 Levantando el Proyecto con Docker (Recomendado)

La forma más sencilla de correr el proyecto completo es usando Docker Compose. Esto levantará la base de datos, el backend y el frontend automáticamente.

1.  Cloná el repositorio y posicionate en la raíz del proyecto.
2.  Ejecutá el siguiente comando:

    ```bash
    docker-compose up --build
    ```

3.  Accedé a las aplicaciones:
    - **Frontend**: [http://localhost:5173](http://localhost:5173)
    - **Backend (API)**: [http://localhost:8000](http://localhost:8000)
    - **Documentación Swagger**: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 💻 Configuración para Desarrollo Local

Si preferís levantar los servicios de forma manual (sin Docker):

### 1. Base de Datos

Necesitás una instancia de PostgreSQL corriendo. Podés usar Docker solo para la DB:

```bash
docker run --name foodstore_db -e POSTGRES_PASSWORD=password -e POSTGRES_DB=foodstore_db -p 5432:5432 -d postgres:15-alpine
```

### 2. Backend

Navegá a la carpeta `backend/`:

```bash
cd backend
python -m venv .venv
# Activar entorno (Windows)
.venv\Scripts\activate
# Activar entorno (Linux/macOS)
source .venv/bin/activate

pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

### 3. Frontend

Navegá a la carpeta `frontend/`:

```bash
cd frontend
npm install
npm run dev
```

---

## 📁 Estructura del Proyecto

```text
trabajo_practico_4/
├── backend/            # API con FastAPI y SQLModel
│   ├── app/            # Código fuente del backend
│   └── requirements.txt
├── frontend/           # Aplicación React con Vite
│   ├── src/            # Código fuente del frontend
│   └── package.json
└── docker-compose.yml  # Orquestación de contenedores
```

## 📝 Notas Adicionales

- El archivo `backend/rest-client.http` incluye ejemplos de peticiones para probar la API rápidamente si usas la extensión REST Client en VS Code.
- Asegurate de configurar las variables de entorno si decidís cambiar las credenciales de la base de datos.

---

_Desarrollado para la cátedra de Programación IV - UTN FRM._
