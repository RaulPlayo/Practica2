# Práctica 2 — Backend Python con FastAPI, Arquitectura Limpia e IA

Backend completo en FastAPI que reemplaza el servidor original, manteniendo el contrato de API que consume el frontend Svelte 5 existente.

---

## Contrato de API detectado en el frontend

| Método | Endpoint | Auth | Body / Query | Respuesta esperada |
| :--- | :--- | :---: | :--- | :--- |
| **POST** | `/api/login` | No | `{ username, password }` | `{ token }` |
| **POST** | `/api/register` | No | `{ username, password }` | `201` / `{ message }` |
| **GET** | `/api/productos` | No | `?name=` *(opcional)* | `Product[]` |
| **POST** | `/api/productos` | Bearer (admin) | `FormData` *(nombre, precio, imagen?)* | `Product` |
| **PUT** | `/api/productos/:id` | Bearer (admin) | `{ nombre, precio }` | `Product` |
| **DELETE** | `/api/productos/:id` | Bearer (admin) | — | `200` |
| **GET** | `/api/users` | Bearer (admin) | — | `User[]` |
| **PUT** | `/api/users/:id` | Bearer (admin) | `{ role }` | `User` |
| **DELETE** | `/api/users/:id` | Bearer (admin) | — | `200` |
| **GET** | `/uploads/:filename` | No | — | Archivo estático |

### Modelos de Datos de la API
* **Modelo Product:** `{ _id, nombre, precio, imagen }`
* **Modelo User:** `{ _id, username, role }` *(el password nunca se devuelve)*
* **JWT payload:** `{ id, username, role, exp }`

---

## Arquitectura de capas propuesta

```text
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                  # FastAPI app factory, CORS, mount /uploads
│   ├── config.py                # Settings (SECRET_KEY, DB_URL, etc.)
│   ├── database.py              # SQLAlchemy engine + SessionLocal
│   │
│   ├── models/                  # ORM models (SQLAlchemy)
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── product.py
│   │
│   ├── schemas/                 # Pydantic schemas (validación)
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── product.py
│   │
│   ├── repositories/            # Acceso a datos (patrón repositorio)
│   │   ├── __init__.py
│   │   ├── user_repository.py
│   │   └── product_repository.py
│   │
│   ├── services/                # Lógica de negocio
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── user_service.py
│   │   └── product_service.py
│   │
│   ├── routers/                 # Controladores HTTP
│   │   ├── __init__.py
│   │   ├── auth_router.py
│   │   ├── user_router.py
│   │   └── product_router.py
│   │
│   ├── middleware/               # Dependencias / middlewares
│   │   ├── __init__.py
│   │   └── auth.py              # get_current_user, require_admin
│   │
│   └── exceptions/              # Manejo global de excepciones
│       ├── __init__.py
│       └── handlers.py
│
├── uploads/                     # Carpeta para imágenes subidas
├── requirements.txt
├── seed.py                      # Script para poblar datos iniciales
└── README.md
