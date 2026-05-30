from sqlalchemy.orm import Session
from app.repositories import CartRepository, UserRepository, ProductRepository
from app.core.security import hash_password, verify_password, create_access_token, decode_token
from app.models import User, Product, UserRole


class AuthService:
    """Service for authentication operations - business logic layer."""

    @staticmethod
    def register_user(db: Session, username: str, password: str) -> tuple[User, str]:
        """Register a new user."""
        # Check if user already exists
        existing_user = UserRepository.get_by_username(db, username)
        if existing_user:
            raise ValueError("Usuario ya existe")

        # Hash password
        hashed_password = hash_password(password)

        # Create user with default role
        user = UserRepository.create(
            db,
            username=username,
            hashed_password=hashed_password,
            role=UserRole.USUARIO.value
        )

        # Generate token
        token = create_access_token({
            "id": user.id,
            "username": user.username,
            "role": user.role.value
        })

        return user, token

    @staticmethod
    def login_user(db: Session, username: str, password: str) -> tuple[User, str]:
        """Authenticate a user and return token."""
        # Get user by username
        user = UserRepository.get_by_username(db, username)
        if not user:
            raise ValueError("Credenciales inválidas")

        # Verify password
        if not verify_password(password, user.hashed_password):
            raise ValueError("Credenciales inválidas")

        # Generate token
        token = create_access_token({
            "id": user.id,
            "username": user.username,
            "role": user.role.value
        })

        return user, token

    @staticmethod
    def verify_token(token: str) -> dict:
        """Verify and decode token."""
        payload = decode_token(token)
        if payload is None:
            raise ValueError("Token inválido")
        return payload


class ProductService:
    """Service for product operations - business logic layer."""

    @staticmethod
    def create_product(db: Session, nombre: str, descripcion: str, precio: float, stock: int, imagen: str = None, estado: str = "activo") -> Product:
        """Create a new product."""
        # Validate inputs
        if not nombre or len(nombre.strip()) == 0:
            raise ValueError("El nombre del producto es requerido")

        if precio < 0:
            raise ValueError("El precio no puede ser negativo")

        if stock < 0:
            raise ValueError("El stock no puede ser negativo")

        if estado not in ["activo", "inactivo"]:
            raise ValueError("Estado invalido")

        product = ProductRepository.create(
            db,
            nombre=nombre.strip(),
            descripcion=descripcion or "",
            precio=float(precio),
            stock=int(stock),
            imagen=imagen,
            estado=estado
        )
        return product

    @staticmethod
    def get_product(db: Session, product_id: int) -> Product:
        """Get product by ID."""
        product = ProductRepository.get_by_id(db, product_id)
        if not product:
            raise ValueError("Producto no encontrado")
        return product

    @staticmethod
    def get_all_products(db: Session, skip: int = 0, limit: int = 100) -> list:
        """Get all products."""
        return ProductRepository.get_all(db, skip, limit)

    @staticmethod
    def search_products(db: Session, name: str, skip: int = 0, limit: int = 100) -> list:
        """Search products by name."""
        if not name or len(name.strip()) == 0:
            return ProductRepository.get_all(db, skip, limit)
        return ProductRepository.search_by_name(db, name.strip(), skip, limit)

    @staticmethod
    def update_product(db: Session, product_id: int, **kwargs) -> Product:
        """Update product."""
        product = ProductService.get_product(db, product_id)

        # Validate updates
        if 'precio' in kwargs and kwargs['precio'] is not None:
            if kwargs['precio'] < 0:
                raise ValueError("El precio no puede ser negativo")

        if 'stock' in kwargs and kwargs['stock'] is not None:
            if kwargs['stock'] < 0:
                raise ValueError("El stock no puede ser negativo")

        if 'nombre' in kwargs and kwargs['nombre'] is not None:
            if len(kwargs['nombre'].strip()) == 0:
                raise ValueError("El nombre del producto es requerido")
            kwargs['nombre'] = kwargs['nombre'].strip()

        if 'estado' in kwargs and kwargs['estado'] is not None:
            if kwargs['estado'] not in ["activo", "inactivo"]:
                raise ValueError("Estado invalido")

        updated_product = ProductRepository.update(db, product_id, **kwargs)
        return updated_product

    @staticmethod
    def delete_product(db: Session, product_id: int) -> bool:
        """Delete a product."""
        # Verify product exists
        ProductService.get_product(db, product_id)
        return ProductRepository.delete(db, product_id)


class UserService:
    """Service for user operations - business logic layer."""

    @staticmethod
    def get_user(db: Session, user_id: int) -> User:
        """Get user by ID."""
        user = UserRepository.get_by_id(db, user_id)
        if not user:
            raise ValueError("Usuario no encontrado")
        return user

    @staticmethod
    def get_all_users(db: Session, skip: int = 0, limit: int = 100) -> list:
        """Get all users."""
        return UserRepository.get_all(db, skip, limit)

    @staticmethod
    def update_user(db: Session, user_id: int, **kwargs) -> User:
        """Update user."""
        user = UserService.get_user(db, user_id)

        # Validate updates
        if 'password' in kwargs and kwargs['password']:
            kwargs['hashed_password'] = hash_password(kwargs.pop('password'))

        updated_user = UserRepository.update(db, user_id, **kwargs)
        return updated_user

    @staticmethod
    def delete_user(db: Session, user_id: int) -> bool:
        """Delete a user."""
        UserService.get_user(db, user_id)
        return UserRepository.delete(db, user_id)

    @staticmethod
    def change_user_role(db: Session, user_id: int, role: str) -> User:
        """Change user role (admin only)."""
        if role not in [r.value for r in UserRole]:
            raise ValueError(f"Rol inválido: {role}")

        user = UserService.get_user(db, user_id)
        updated_user = UserRepository.update(db, user_id, role=role)
        return updated_user


class CartService:
    """Service for shopping cart operations."""

    @staticmethod
    def get_cart(db: Session, user_id: int) -> list:
        """Get a user's cart."""
        UserService.get_user(db, user_id)
        return CartRepository.get_items(db, user_id)

    @staticmethod
    def add_to_cart(db: Session, user_id: int, product_id: int) -> list:
        """Add an active product to a user's cart."""
        product = ProductService.get_product(db, product_id)
        if product.estado != "activo":
            raise ValueError("No se puede anadir un producto inactivo")

        CartRepository.add_item(db, user_id, product_id)
        return CartRepository.get_items(db, user_id)

    @staticmethod
    def remove_from_cart(db: Session, user_id: int, product_id: int) -> list:
        """Remove a product from the cart."""
        CartRepository.remove_item(db, user_id, product_id)
        return CartRepository.get_items(db, user_id)

    @staticmethod
    def checkout(db: Session, user_id: int) -> dict:
        """Simulate checkout and clear the cart."""
        items = CartRepository.get_items(db, user_id)
        total = sum((item.product.precio if item.product else 0) * item.quantity for item in items)
        item_count = sum(item.quantity for item in items)
        CartRepository.clear_cart(db, user_id)
        return {
            "message": f"Compra simulada correctamente con {item_count} articulos.",
            "total": round(total, 2),
            "items": item_count,
        }
