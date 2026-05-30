from pydantic import BaseModel, Field, field_validator
from typing import Optional, Literal
from datetime import datetime


# ==================== Auth Schemas ====================

class LoginRequest(BaseModel):
    """Schema for login request."""
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6, max_length=100)


class RegisterRequest(BaseModel):
    """Schema for registration request."""
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6, max_length=100)


class TokenResponse(BaseModel):
    """Schema for token response."""
    token: str
    user: Optional[dict] = None


# ==================== User Schemas ====================

class UserBase(BaseModel):
    """Base user schema."""
    username: str = Field(..., min_length=3, max_length=50)


class UserCreate(UserBase):
    """Schema for user creation."""
    password: str = Field(..., min_length=6, max_length=100)


class UserUpdate(BaseModel):
    """Schema for user update."""
    password: Optional[str] = Field(None, min_length=6, max_length=100)
    role: Optional[Literal["usuario", "admin"]] = None


class UserResponse(UserBase):
    """Schema for user response."""
    id: int
    role: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ==================== Product Schemas ====================

class ProductBase(BaseModel):
    """Base product schema."""
    nombre: str = Field(..., min_length=1, max_length=200)
    descripcion: Optional[str] = Field(default="", max_length=1000)
    precio: float = Field(..., gt=0)
    stock: int = Field(default=0, ge=0)
    estado: Literal["activo", "inactivo"] = "activo"

    @field_validator('precio')
    @classmethod
    def validate_precio(cls, v):
        """Validate that precio is positive."""
        if v < 0:
            raise ValueError('Precio debe ser positivo')
        return round(v, 2)


class ProductCreate(ProductBase):
    """Schema for product creation."""
    pass


class ProductUpdate(BaseModel):
    """Schema for product update."""
    nombre: Optional[str] = Field(None, min_length=1, max_length=200)
    descripcion: Optional[str] = Field(None, max_length=1000)
    precio: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    estado: Optional[Literal["activo", "inactivo"]] = None

    @field_validator('precio')
    @classmethod
    def validate_precio(cls, v):
        """Validate that precio is positive."""
        if v is not None and v < 0:
            raise ValueError('Precio debe ser positivo')
        return round(v, 2) if v is not None else v


class ProductResponse(ProductBase):
    """Schema for product response."""
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ==================== Error Response Schemas ====================

class ErrorResponse(BaseModel):
    """Schema for error response."""
    detail: str
    status_code: int
