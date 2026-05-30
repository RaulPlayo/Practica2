from fastapi import APIRouter, Depends, Header, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.security import decode_token
from app.schemas import UserResponse, UserUpdate
from app.services import UserService

router = APIRouter(prefix="/api", tags=["users"])


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


@router.get("/users")
def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin)
):
    """
    Get all users (admin only).
    
    **CAPA: ROUTER (Controller)**
    - Requires admin authentication
    - Calls UserService to get all users
    """
    try:
        users = UserService.get_all_users(db, skip, limit)
        return [user.to_dict() for user in users]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener usuarios"
        )


@router.get("/users/{user_id}")
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_auth)
):
    """
    Get a specific user by ID (authenticated users).
    
    **CAPA: ROUTER (Controller)**
    - Requires authentication
    - Users can only see their own data, admins can see any user
    """
    try:
        # Check authorization
        if current_user.get("id") != user_id and current_user.get("role") != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acceso denegado"
            )

        user = UserService.get_user(db, user_id)
        return user.to_dict()
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al obtener usuario"
        )


@router.put("/users/{user_id}")
def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_auth)
):
    """
    Update user data (authenticated users).
    
    **CAPA: ROUTER (Controller)**
    - Requires authentication
    - Users can only update their own data
    - Only admins can change roles
    """
    try:
        # Check authorization
        if current_user.get("id") != user_id and current_user.get("role") != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acceso denegado"
            )

        update_data = user_data.dict(exclude_unset=True)

        # Only admins can change roles
        if "role" in update_data and current_user.get("role") != "admin":
            del update_data["role"]

        updated_user = UserService.update_user(db, user_id, **update_data)
        return updated_user.to_dict()
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al actualizar usuario"
        )


@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin)
):
    """
    Delete a user (admin only).
    
    **CAPA: ROUTER (Controller)**
    - Requires admin authentication
    """
    try:
        UserService.delete_user(db, user_id)
        return {"message": "Usuario eliminado correctamente"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al eliminar usuario"
        )


@router.patch("/users/{user_id}/role")
def change_user_role(
    user_id: int,
    role_data: dict,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin)
):
    """
    Change user role (admin only).
    
    **CAPA: ROUTER (Controller)**
    - Requires admin authentication
    - Expected body: {"role": "admin" or "usuario"}
    """
    try:
        role = role_data.get("role")
        if not role:
            raise ValueError("Role es requerido")

        updated_user = UserService.change_user_role(db, user_id, role)
        return updated_user.to_dict()
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al cambiar rol"
        )
