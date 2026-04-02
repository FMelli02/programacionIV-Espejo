## 🚀 Backend (FastAPI)

Ubicación: `fastapi-productos/`

### 1) Crear entorno virtual

```bash
cd fastapi-productos
python -m venv .venv
```

### 2) Activar entorno

- **Windows**

```bash
.venv\Scripts\activate
```

- **macOS/Linux**

```bash
source .venv/bin/activate
```

### 3) Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4) Levantar servidor

```bash
python -m uvicorn app.main:app --reload
```

Backend corriendo en: `http://localhost:8000`

Swagger docs: `http://localhost:8000/docs`

---

## 🌐 Frontend (React + TypeScript + Tailwind)

Ubicación: `tp-categorias/`

### 1) Instalar dependencias

```bash
cd tp-categorias
pnpm install
```

### 2) Ejecutar modo desarrollo

```bash
pnpm dev
```

Frontend corriendo en: `http://localhost:5173`