# Practica 2 - Backend FastAPI

Backend desarrollado en Python con FastAPI para sustituir el backend original del
frontend Svelte 5 de la Practica 2.

## Objetivo

El servidor mantiene el contrato que consume el frontend:

- API REST bajo `/api`.
- Autenticacion mediante JWT.
- Productos con CRUD completo.
- Usuarios con CRUD completo y roles `usuario` / `admin`.
- Carrito por usuario autenticado.
- Respuestas de productos y usuarios con campo `_id` para compatibilidad con el frontend.

## Arquitectura

El codigo esta separado en capas:

```text
backend/
  app/
    core/            Configuracion de BD y seguridad JWT
    models/          Modelos ORM de SQLAlchemy
    repositories/    Acceso a datos
    services/        Logica de negocio
    routers/         Endpoints HTTP
    schemas/         Validacion con Pydantic
    main.py          Aplicacion FastAPI y manejadores globales
  init_db.py         Inicializacion con datos de prueba
  requirements.txt
```

Los routers solo gestionan HTTP, validacion de entrada y dependencias de seguridad.
La logica de negocio vive en `services` y las consultas SQL estan encapsuladas en
`repositories`.

## Instalacion

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python init_db.py
```

## Ejecucion

```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 3000 --reload
```

La API queda disponible en:

- API: `http://localhost:3000/api`
- Documentacion Swagger: `http://localhost:3000/docs`
- Health check: `http://localhost:3000/health`

## Usuarios de prueba

Al ejecutar `python init_db.py` se crean:

| Usuario | Password | Rol |
| --- | --- | --- |
| `admin` | `admin123` | `admin` |
| `usuario` | `usuario123` | `usuario` |

## Endpoints principales

### Autenticacion

| Metodo | Endpoint | Descripcion |
| --- | --- | --- |
| POST | `/api/register` | Registro de usuario |
| POST | `/api/login` | Login y generacion de JWT |

El token contiene `id`, `username`, `role`, `iat` y `exp`.

### Productos

| Metodo | Endpoint | Rol | Descripcion |
| --- | --- | --- | --- |
| GET | `/api/productos` | Publico | Listar productos |
| GET | `/api/productos?name=texto` | Publico | Buscar por nombre |
| GET | `/api/productos/{id}` | Publico | Ver detalle |
| POST | `/api/productos` | `admin` | Crear producto con `multipart/form-data` |
| PUT | `/api/productos/{id}` | `admin` | Editar producto con `multipart/form-data` |
| DELETE | `/api/productos/{id}` | `admin` | Eliminar producto |

El alta y edicion de productos aceptan `nombre`, `precio`, `descripcion`, `stock`,
`estado` (`activo` o `inactivo`) e `imagen` opcional. Las imagenes se sirven desde
`/uploads/{archivo}`.

### Usuarios

| Metodo | Endpoint | Rol | Descripcion |
| --- | --- | --- | --- |
| GET | `/api/users` | `admin` | Listar usuarios |
| GET | `/api/users/{id}` | Usuario propio o `admin` | Ver usuario |
| PUT | `/api/users/{id}` | Usuario propio o `admin` | Cambiar password; admin tambien puede cambiar rol |
| DELETE | `/api/users/{id}` | `admin` | Eliminar usuario |
| PATCH | `/api/users/{id}/role` | `admin` | Cambiar rol |

### Carrito

| Metodo | Endpoint | Rol | Descripcion |
| --- | --- | --- | --- |
| GET | `/api/cart` | Usuario autenticado | Ver carrito |
| POST | `/api/cart/add` | Usuario autenticado | Anadir producto con `{ "productId": id }` |
| DELETE | `/api/cart/{product_id}` | Usuario autenticado | Eliminar producto del carrito |
| POST | `/api/cart/checkout` | Usuario autenticado | Simular compra y vaciar carrito |

## Funcionalidades avanzadas

- Validacion estricta con Pydantic y parametros `Form`.
- Manejo global de errores: validacion `422`, autenticacion `401`, permisos `403` y errores inesperados `500`.
- Persistencia real en SQLite con SQLAlchemy.
- Patron repositorio para aislar las consultas de base de datos.
- Hash de passwords con bcrypt.
- JWT con `python-jose`.

## Memoria de IA

La memoria del uso de IA esta en `../MEMORIA_IA.md` e incluye prompts, iteraciones,
errores detectados y correcciones manuales.
