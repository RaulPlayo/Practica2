from fastapi import APIRouter, Depends, File, Form, Header, HTTPException, UploadFile, status, Query
from sqlalchemy.orm import Session
from pathlib import Path
from uuid import uuid4

from app.core.database import get_db
from app.core.security import decode_token
from app.services import ProductService

router = APIRouter(prefix="/api", tags=["productos"])
UPLOAD_DIR = Path("uploads")
ALLOWED_IMAGE_TYPES = {"image/jpeg": ".jpg", "image/png": ".png", "image/webp": ".webp", "image/gif": ".gif"}


def get_current_user(authorization: str | None = Header(default=None)):
    """Extract current user from Authorization header."""
    if not authorization:
        return None

    try:
        token = authorization.replace("Bearer ", "")
        payload = decode_token(token)
        if payload is None:
            return None
        return payload
    except Exception:
        return None


def require_auth(current_user: dict = Depends(get_current_user)):
    """Dependency to require authentication."""
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No autorizado"
        )
    return current_user


def require_admin(current_user: dict = Depends(require_auth)):
    """Dependency to require admin role."""
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso denegado - se requiere rol administrador"
        )
    return current_user


@router.get("/productos")
def list_products(
    name: str = Query(None, description="Filtrar por nombre"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """
    Get all products or search by name.
    
    **CAPA: ROUTER (Controller)**
    - Public endpoint (no auth required)
    - Calls ProductService to get products
    - Returns list of products
    """
    try:
        if name:
            products = ProductService.search_products(db, name, skip, limit)
        else:
            products = ProductService.get_all_products(db, skip, limit)

        # Convert to dict format matching frontend expectations
        return [product.to_dict() for product in products]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener productos"
        )


@router.get("/productos/{product_id}")
def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific product by ID.
    
    **CAPA: ROUTER (Controller)**
    - Public endpoint
    - Calls ProductService to get product
    """
    try:
        product = ProductService.get_product(db, product_id)
        return product.to_dict()
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener producto"
        )


def save_uploaded_image(imagen: UploadFile | None) -> str | None:
    if imagen is None or not imagen.filename:
        return None

    extension = ALLOWED_IMAGE_TYPES.get(imagen.content_type)
    if extension is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="La imagen debe ser JPG, PNG, WEBP o GIF"
        )

    UPLOAD_DIR.mkdir(exist_ok=True)
    filename = f"{uuid4().hex}{extension}"
    destination = UPLOAD_DIR / filename
    with destination.open("wb") as output:
        output.write(imagen.file.read())
    return filename


@router.post("/productos")
def create_product(
    nombre: str = Form(..., min_length=1, max_length=200),
    precio: float = Form(..., gt=0),
    descripcion: str = Form(default="", max_length=1000),
    stock: int = Form(default=0, ge=0),
    estado: str = Form(default="activo"),
    imagen: UploadFile | None = File(default=None),
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin)
):
    """
    Create a new product (admin only).
    
    **CAPA: ROUTER (Controller)**
    - Requires authentication and admin role
    - Validates input with Pydantic
    - Calls ProductService for business logic
    """
    try:
        image_filename = save_uploaded_image(imagen)
        new_product = ProductService.create_product(
            db,
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
            stock=stock,
            imagen=image_filename,
            estado=estado
        )
        return new_product.to_dict()
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al crear producto"
        )


@router.put("/productos/{product_id}")
def update_product(
    product_id: int,
    nombre: str | None = Form(default=None, min_length=1, max_length=200),
    precio: float | None = Form(default=None, gt=0),
    descripcion: str | None = Form(default=None, max_length=1000),
    stock: int | None = Form(default=None, ge=0),
    estado: str | None = Form(default=None),
    imagen: UploadFile | None = File(default=None),
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin)
):
    """
    Update a product (admin only).
    
    **CAPA: ROUTER (Controller)**
    - Requires authentication and admin role
    - Validates input with Pydantic
    - Calls ProductService for business logic
    """
    try:
        update_data = {
            key: value
            for key, value in {
                "nombre": nombre,
                "precio": precio,
                "descripcion": descripcion,
                "stock": stock,
                "estado": estado,
            }.items()
            if value is not None
        }
        image_filename = save_uploaded_image(imagen)
        if image_filename:
            update_data["imagen"] = image_filename

        updated_product = ProductService.update_product(db, product_id, **update_data)
        return updated_product.to_dict()
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al actualizar producto"
        )


@router.delete("/productos/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin)
):
    """
    Delete a product (admin only).
    
    **CAPA: ROUTER (Controller)**
    - Requires authentication and admin role
    - Calls ProductService for business logic
    """
    try:
        ProductService.delete_product(db, product_id)
        return {"message": "Producto eliminado correctamente"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al eliminar producto"
        )
