from pathlib import Path

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from app.core.database import init_db
from app.routers import auth, cart, productos, users


UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

app = FastAPI(
    title="Practica 2 Backend",
    description="Backend para Practica 2 - FastAPI, arquitectura limpia e IA",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://localhost:80",
        "http://localhost:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Convert Pydantic validation errors into a consistent API response."""
    errors = [
        {
            "field": ".".join(str(part) for part in error["loc"][1:]),
            "message": error["msg"],
            "type": error["type"],
        }
        for error in exc.errors()
    ]

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "message": "Error de validacion",
            "detail": "Error de validacion",
            "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
            "errors": errors,
        },
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Return a unified JSON shape for controlled HTTP errors."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "message": exc.detail,
            "detail": exc.detail,
            "status_code": exc.status_code,
        },
        headers=exc.headers,
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Avoid leaking traces in unexpected server errors."""
    print(f"Error no controlado: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "message": "Error interno del servidor",
            "detail": "Error interno del servidor",
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
        },
    )


@app.on_event("startup")
def startup_event():
    """Initialize database on startup."""
    print("Inicializando base de datos...")
    init_db()
    print("Base de datos inicializada")


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "ok", "message": "Backend operativo"}


app.include_router(auth.router)
app.include_router(productos.router)
app.include_router(users.router)
app.include_router(cart.router)


@app.get("/")
def root():
    """Root endpoint with API information."""
    return {
        "name": "Practica 2 Backend",
        "description": "Backend para Practica 2 - FastAPI, arquitectura limpia e IA",
        "version": "1.0.0",
        "endpoints": {
            "auth": ["POST /api/register", "POST /api/login"],
            "productos": [
                "GET /api/productos",
                "GET /api/productos/{id}",
                "POST /api/productos (admin, multipart/form-data)",
                "PUT /api/productos/{id} (admin)",
                "DELETE /api/productos/{id} (admin)",
            ],
            "users": [
                "GET /api/users (admin)",
                "GET /api/users/{id} (auth)",
                "PUT /api/users/{id} (auth/admin)",
                "DELETE /api/users/{id} (admin)",
                "PATCH /api/users/{id}/role (admin)",
            ],
            "cart": [
                "GET /api/cart (auth)",
                "POST /api/cart/add (auth)",
                "DELETE /api/cart/{product_id} (auth)",
                "POST /api/cart/checkout (auth)",
            ],
        },
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=3000, reload=True)
