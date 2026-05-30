# Memoria del uso de Inteligencia Artificial - Practica 2

## 1. Contexto

Para esta practica se utilizo IA como asistente de desarrollo para construir un backend
en Python con FastAPI compatible con el frontend Svelte 5 existente. La IA se uso para
proponer estructura, revisar contratos de API, generar partes repetitivas y detectar
posibles fallos, pero las decisiones finales se comprobaron manualmente contra el
codigo del frontend y el enunciado.

## 2. Registro de prompts e iteraciones

### Prompt 1 - Estructura inicial por capas

**Prompt enviado:**

> Tengo un frontend en Svelte 5 que consume una API REST en `http://localhost:3000/api`.
> Necesito reemplazar el backend por uno en Python con FastAPI. Organiza el codigo en
> capas `routers`, `services`, `repositories`, `models`, `schemas` y `core`. Los routers
> no deben contener queries SQL ni logica de negocio compleja.

**Respuesta obtenida de la IA:**

La IA propuso una estructura modular con `app/main.py`, routers separados para
autenticacion, productos y usuarios, servicios para la logica de negocio y repositorios
para SQLAlchemy.

**Problema detectado:**

La primera respuesta dejaba demasiada logica en los routers, especialmente validaciones
de existencia y reglas de roles mezcladas con operaciones de base de datos.

**Refinamiento enviado:**

> Refactoriza para que los routers solo manejen HTTP y dependencias. Las comprobaciones
> de negocio deben ir en servicios y las queries solo en repositorios. Manten nombres
> sencillos y compatibles con una practica academica.

**Resultado final aplicado:**

Se separaron las responsabilidades:

- `routers`: endpoints, dependencias, codigos HTTP.
- `services`: login, registro, validaciones de negocio, permisos de actualizacion.
- `repositories`: CRUD con SQLAlchemy.
- `models`: tablas ORM.
- `schemas`: validacion Pydantic.

### Prompt 2 - JWT compatible con el frontend

**Prompt enviado:**

> El frontend guarda el token en localStorage y lo divide con `atob()` para obtener
> directamente `id`, `username` y `role`. Genera un sistema JWT con `python-jose` y
> bcrypt. El payload debe ser compatible con ese frontend.

**Respuesta obtenida de la IA:**

La IA genero funciones para crear y validar JWT, pero incluyo el usuario principal en
`sub`, siguiendo una convencion comun de JWT.

**Problema detectado:**

El frontend no lee `sub`; lee `payload.id`, `payload.username` y `payload.role`.

**Refinamiento enviado:**

> No uses solo `sub`. El token debe incluir exactamente los campos que lee el frontend:
> `id`, `username`, `role`, ademas de `iat` y `exp`.

**Resultado final aplicado:**

El token generado contiene:

```json
{
  "id": 1,
  "username": "admin",
  "role": "admin",
  "iat": 1710000000,
  "exp": 1710086400
}
```

### Prompt 3 - Contrato de API con Svelte

**Prompt enviado:**

> Revisa este store de Svelte: crea productos usando `FormData`, envia el token en el
> header `Authorization: Bearer <token>` y usa `_id` en productos y usuarios. Ajusta el
> backend para que sea compatible sin cambiar la logica principal del frontend.

**Respuesta obtenida de la IA:**

La IA propuso endpoints JSON normales para productos y respuestas con `id`.

**Problema detectado:**

El frontend envia `multipart/form-data` al crear productos y renderiza listas usando
`product._id` y `user._id`. Si el backend devuelve solo `id`, la interfaz falla.

**Refinamiento enviado:**

> El endpoint `POST /api/productos` debe aceptar `FormData` con `nombre`, `precio` e
> `imagen` opcional. Las respuestas deben incluir `_id`. Los endpoints privados deben
> leer el header real `Authorization`.

**Resultado final aplicado:**

Se ajusto `POST /api/productos` para usar `Form(...)` y `File(...)`, se anadio `_id` en
las respuestas y se corrigieron las dependencias con `Header(default=None)`.

### Prompt 4 - Validacion estricta y errores

**Prompt enviado:**

> Implementa validacion estricta para productos y usuarios en FastAPI. Productos:
> nombre obligatorio, precio mayor que 0, stock mayor o igual que 0. Usuarios:
> username y password con longitudes minimas. Los errores deben responder con JSON
> estructurado y codigos HTTP correctos.

**Respuesta obtenida de la IA:**

La IA propuso usar Pydantic con `Field`, `Literal` para roles y un handler para
`RequestValidationError`.

**Refinamiento enviado:**

> Anade tambien un manejador para `HTTPException` y un manejador generico para 500, de
> forma que todas las respuestas de error tengan `message`, `detail` y `status_code`.

**Resultado final aplicado:**

El backend devuelve errores uniformes para validacion, autenticacion, permisos y errores
inesperados.

### Prompt 5 - Persistencia y patron repositorio

**Prompt enviado:**

> Sustituye cualquier array en memoria por SQLite con SQLAlchemy. Usa patron repositorio:
> los servicios no deben importar SQLAlchemy ni construir queries directamente. Incluye
> CRUD de productos y usuarios.

**Respuesta obtenida de la IA:**

La IA genero modelos `User` y `Product`, repositorios CRUD y configuracion SQLite.

**Problema detectado:**

En una primera version faltaba refrescar las entidades tras `commit`, lo que podia
devolver objetos sin valores actualizados generados por la base de datos.

**Refinamiento enviado:**

> Tras cada `commit()` de creacion o actualizacion, llama a `db.refresh(entidad)` antes
> de devolver el objeto.

**Resultado final aplicado:**

Los metodos de escritura en repositorios hacen `commit()` y `refresh()` antes de
devolver entidades.

### Prompt 6 - Integracion con el frontend definitivo de la Practica 1

**Prompt enviado:**

> He sustituido el frontend por el de la Practica 1. Revisa su store de Svelte y dime
> que contrato de API espera. No cambies lo que ya funciona segun la Practica 2; adapta
> solo los puntos necesarios del backend FastAPI.

**Respuesta obtenida de la IA:**

La IA detecto que el nuevo frontend ya no solo consumia productos y usuarios, sino que
tambien esperaba un carrito con rutas `/api/cart`, `/api/cart/add`,
`/api/cart/{productId}` y `/api/cart/checkout`. Tambien detecto que la edicion de
productos enviaba `FormData` y que los productos tenian campo `estado`.

**Refinamiento enviado:**

> Manteniendo la arquitectura por capas, anade un modelo de carrito persistido en
> SQLite, repositorio, servicio y router. Los productos deben soportar `estado` activo o
> inactivo y el `PUT /api/productos/{id}` debe aceptar multipart/form-data.

**Resultado final aplicado:**

Se anadio `CartItem` en SQLAlchemy, `CartRepository`, `CartService` y `cart.py` como
router. Ademas, se amplio el modelo `Product` con `estado` y se adapto la actualizacion
de productos para aceptar `FormData`, imagen opcional y estado.

## 3. Analisis critico de errores de la IA

### Error 1 - Uso incorrecto del header Authorization

La IA genero dependencias como:

```python
def get_current_user(authorization: str = None):
    ...
```

Esto parece razonable, pero en FastAPI ese parametro no se lee automaticamente desde
los headers. FastAPI lo interpreta como query parameter si no se indica `Header`.

**Por que era incorrecto:**

Las rutas privadas recibian siempre `authorization=None`, aunque el frontend enviara:

```http
Authorization: Bearer <token>
```

Por tanto, las operaciones de admin podian fallar con `401 No autorizado`.

**Correccion manual aplicada:**

```python
from fastapi import Header

def get_current_user(authorization: str | None = Header(default=None)):
    ...
```

**Concepto aplicado:**

Uso correcto del sistema de dependencias de FastAPI y respeto del contrato HTTP entre
cliente y servidor.

### Error 2 - Respuestas con `id` en vez de `_id`

La IA propuso respuestas tipicas de SQL:

```json
{ "id": 1, "nombre": "Laptop", "precio": 1299.99 }
```

**Por que era incorrecto:**

El frontend venia de una API estilo MongoDB y usaba `_id` para claves de listas,
actualizaciones y borrados.

**Correccion manual aplicada:**

Los metodos `to_dict()` devuelven `_id` junto a `id` para mantener compatibilidad:

```python
return {
    "_id": str(self.id),
    "id": self.id,
    "nombre": self.nombre,
    "precio": self.precio
}
```

**Concepto aplicado:**

Contrato de interfaz. La API nueva debe adaptarse al cliente existente, no al reves.

### Error 3 - Crear productos como JSON cuando el frontend envia FormData

La IA genero inicialmente:

```python
@router.post("/productos")
def create_product(product: ProductCreate):
    ...
```

**Por que era incorrecto:**

El formulario del frontend usa `FormData` porque permite adjuntar una imagen. Si el
backend espera JSON, FastAPI responde `422 Unprocessable Entity`.

**Correccion manual aplicada:**

```python
@router.post("/productos")
def create_product(
    nombre: str = Form(...),
    precio: float = Form(...),
    imagen: UploadFile | None = File(default=None),
):
    ...
```

**Concepto aplicado:**

Validacion adecuada al tipo real de peticion: JSON y `multipart/form-data` no se
procesan igual.

### Error 4 - Rol `user` frente a `usuario`

La IA mezcló valores de rol en ingles (`user`) con el enunciado y la base de datos, que
usan `usuario` y `admin`.

**Por qué era incorrecto:**

Una API con roles inconsistentes puede aceptar un valor en una pantalla y rechazarlo en
otra. Ademas, dificulta comprobar permisos.

**Correccion manual aplicada:**

Se normalizo el backend a `usuario` / `admin` y se ajusto el panel de administracion
para alternar entre esos dos valores.

## 4. Partes desarrolladas con ayuda de IA

- Propuesta de estructura inicial FastAPI.
- Esquemas Pydantic y validaciones.
- Repositorios SQLAlchemy.
- Servicio de autenticacion con JWT.
- Manejadores globales de excepciones.

## 5. Partes revisadas o corregidas manualmente

- Lectura real del header `Authorization`.
- Compatibilidad con `_id`.
- Endpoint de creacion de productos con `FormData`.
- Roles `usuario` / `admin`.
- Persistencia de imagen opcional.
- Carrito persistido por usuario para el frontend definitivo.
- Campo `estado` y edicion de productos mediante `FormData`.
- Revision del contrato entre frontend y backend.

## 6. Conclusion

La IA fue util para acelerar la estructura y generar primeras versiones, pero requirio
revision critica. Los errores principales no eran de sintaxis, sino de contexto: asumir
convenciones genericas sin comprobar como trabaja el frontend existente. La mejora clave
fue contrastar cada propuesta con el contrato real de la aplicacion y con los conceptos
vistos en clase: separacion de capas, validacion, autenticacion, manejo de errores y
persistencia mediante repositorios.
