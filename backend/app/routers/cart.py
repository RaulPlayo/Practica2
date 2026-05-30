from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_token
from app.services import CartService


router = APIRouter(prefix="/api", tags=["cart"])


def get_current_user(authorization: str | None = Header(default=None)):
    """Extract current user from Authorization header."""
    if not authorization:
        return None

    try:
        token = authorization.replace("Bearer ", "")
        return decode_token(token)
    except Exception:
        return None


def require_auth(current_user: dict = Depends(get_current_user)):
    """Dependency to require authentication."""
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No autorizado",
        )
    return current_user


def cart_response(items):
    """Serialize cart items in the format expected by the frontend."""
    return [item.to_dict() for item in items]


@router.get("/cart")
def get_cart(
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_auth),
):
    """Get the current user's cart."""
    return cart_response(CartService.get_cart(db, current_user["id"]))


@router.post("/cart/add")
def add_to_cart(
    payload: dict,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_auth),
):
    """Add one unit of a product to the current user's cart."""
    product_id = payload.get("productId")
    if product_id is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="productId es requerido",
        )

    try:
        return cart_response(CartService.add_to_cart(db, current_user["id"], int(product_id)))
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        )


@router.delete("/cart/{product_id}")
def remove_from_cart(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_auth),
):
    """Remove a product from the current user's cart."""
    return cart_response(CartService.remove_from_cart(db, current_user["id"], product_id))


@router.post("/cart/checkout")
def checkout(
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_auth),
):
    """Simulate checkout and clear the current user's cart."""
    return CartService.checkout(db, current_user["id"])
