# Práctica 2 — Backend Python con FastAPI, Arquitectura Limpia e IA

Backend completo en FastAPI que reemplaza el servidor original, manteniendo el contrato de API que consume el frontend Svelte 5 existente. Cubre los 10 puntos del enunciado.

## Contrato de API detectado en el frontend

| Método   | Endpoint            | Auth          | Body / Query                          | Respuesta esperada           |
|----------|---------------------|---------------|---------------------------------------|------------------------------|
| POST     | `/api/login`        | No            | `{ username, password }`              | `{ token }`                  |
| POST     | `/api/register`     | No            | `{ username, password }`              | `201 / { message }`          |
| GET      | `/api/productos`    | No            | `?name=` (opcional)                   | `Product[]`                  |
| POST     | `/api/productos`    | Bearer (admin) | `FormData(nombre, precio, imagen?)`   | `Product`                    |
| PUT      | `/api/productos/:id`| Bearer (admin) | `{ nombre, precio }`                  | `Product`                    |
| DELETE   | `/api/productos/:id`| Bearer (admin) | —                                     | `200`                        |
| GET      | `/api/users`        | Bearer (admin) | —                                     | `User[]`                     |
| PUT      | `/api/users/:id`    | Bearer (admin) | `{ role }`                            | `User`                       |
| DELETE   | `/api/users/:id`    | Bearer (admin) | —                                     | `200`                        |
| GET      | `/uploads/:filename`| No            | —                                     | archivo estático             |

**Modelos:**

- `Product`: `{ _id, nombre, precio, imagen }`
- `User`: `{ _id, username, role }` (password nunca se devuelve)
- JWT payload: `{ id, username, role, exp }`

## Arquitectura de capas propuesta
