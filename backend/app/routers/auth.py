from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_token
from app.schemas import LoginRequest, RegisterRequest, TokenResponse, UserResponse
from app.services import AuthService

router = APIRouter(prefix="/api", tags=["auth"])


def get_current_user(db: Session = Depends(get_db)):
    """Dependency to get current user from token."""
    async def verify_token(authorization: str | None = Header(default=None)):
        if not authorization:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No autorizado"
            )

        try:
            token = authorization.replace("Bearer ", "")
            payload = decode_token(token)
            if payload is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token inválido"
                )
            return payload
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No autorizado"
            )

    return verify_token


def require_admin(current_user: dict = Depends(get_current_user)):
    """Dependency to require admin role."""
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso denegado - se requiere rol administrador"
        )
    return current_user


@router.post("/register", response_model=TokenResponse)
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    """
    Register a new user.
    
    **CAPA: ROUTER (Controller)**
    - Validates input with Pydantic
    - Calls AuthService for business logic
    - Returns response
    """
    try:
        user, token = AuthService.register_user(db, request.username, request.password)
        return TokenResponse(
            token=token,
            user={
                "id": user.id,
                "username": user.username,
                "role": user.role.value
            }
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error en el registro"
        )


@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    Login a user and return JWT token.
    
    **CAPA: ROUTER (Controller)**
    - Validates input with Pydantic
    - Calls AuthService for business logic
    - Returns JWT token
    """
    try:
        user, token = AuthService.login_user(db, request.username, request.password)
        return TokenResponse(
            token=token,
            user={
                "id": user.id,
                "username": user.username,
                "role": user.role.value
            }
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error en la autenticación"
        )
