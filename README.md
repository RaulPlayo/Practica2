# Practica 2 - Backend Python con FastAPI

Proyecto de la Practica 2 de Programacion Web. El frontend esta hecho con Svelte 5 y el
backend se ha reemplazado por una API en Python con FastAPI.

![Panel principal](/backend/uploads/panel.png)

## Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python init_db.py
python -m uvicorn app.main:app --host 0.0.0.0 --port 3000 --reload
```

API: `http://localhost:3000/api`

Swagger: `http://localhost:3000/docs`

Credenciales de prueba:

- Admin: `admin` / `admin123`
- Usuario: `usuario` / `usuario123`

![Panel de administrador](/backend/uploads/panelAdmin.png)

## Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend: `http://localhost:8000`

![Panel de administrador](/backend/uploads/carrito.png)

## Funcionalidades principales

- JWT compatible con el frontend.
- CRUD de productos protegido por rol `admin`.
- Productos con imagen opcional y estado `activo` / `inactivo`.
- CRUD de usuarios con roles `usuario` y `admin`.
- Carrito por usuario: anadir, eliminar y simular compra.
- Validacion con Pydantic.
- Manejo global de errores.
- SQLite con SQLAlchemy y patron repositorio.
- Documentacion del uso de IA en `MEMORIA_IA.md`.
