from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models import CartItem, User, Product


class UserRepository:
    """Repository pattern for User model - data access layer."""

    @staticmethod
    def create(db: Session, username: str, hashed_password: str, role: str = "usuario") -> User:
        """Create a new user."""
        user = User(username=username, hashed_password=hashed_password, role=role)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def get_by_id(db: Session, user_id: int) -> User:
        """Get user by ID."""
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_by_username(db: Session, username: str) -> User:
        """Get user by username."""
        return db.query(User).filter(User.username == username).first()

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> list:
        """Get all users with pagination."""
        return db.query(User).offset(skip).limit(limit).all()

    @staticmethod
    def update(db: Session, user_id: int, **kwargs) -> User:
        """Update user fields."""
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            for key, value in kwargs.items():
                if hasattr(user, key) and value is not None:
                    setattr(user, key, value)
            db.commit()
            db.refresh(user)
        return user

    @staticmethod
    def delete(db: Session, user_id: int) -> bool:
        """Delete a user."""
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            db.delete(user)
            db.commit()
            return True
        return False


class ProductRepository:
    """Repository pattern for Product model - data access layer."""

    @staticmethod
    def create(db: Session, nombre: str, descripcion: str, precio: float, stock: int = 0, imagen: str = None, estado: str = "activo") -> Product:
        """Create a new product."""
        product = Product(
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
            stock=stock,
            imagen=imagen,
            estado=estado
        )
        db.add(product)
        db.commit()
        db.refresh(product)
        return product

    @staticmethod
    def get_by_id(db: Session, product_id: int) -> Product:
        """Get product by ID."""
        return db.query(Product).filter(Product.id == product_id).first()

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> list:
        """Get all products with pagination."""
        return db.query(Product).offset(skip).limit(limit).all()

    @staticmethod
    def search_by_name(db: Session, name: str, skip: int = 0, limit: int = 100) -> list:
        """Search products by name (case-insensitive)."""
        return db.query(Product).filter(
            Product.nombre.ilike(f"%{name}%")
        ).offset(skip).limit(limit).all()

    @staticmethod
    def update(db: Session, product_id: int, **kwargs) -> Product:
        """Update product fields."""
        product = db.query(Product).filter(Product.id == product_id).first()
        if product:
            for key, value in kwargs.items():
                if hasattr(product, key) and value is not None:
                    setattr(product, key, value)
            db.commit()
            db.refresh(product)
        return product

    @staticmethod
    def delete(db: Session, product_id: int) -> bool:
        """Delete a product."""
        product = db.query(Product).filter(Product.id == product_id).first()
        if product:
            db.delete(product)
            db.commit()
            return True
        return False

    @staticmethod
    def exists(db: Session, product_id: int) -> bool:
        """Check if product exists."""
        return db.query(Product).filter(Product.id == product_id).first() is not None


class CartRepository:
    """Repository pattern for CartItem model."""

    @staticmethod
    def get_items(db: Session, user_id: int) -> list[CartItem]:
        """Get cart items for a user."""
        return db.query(CartItem).filter(CartItem.user_id == user_id).all()

    @staticmethod
    def get_item(db: Session, user_id: int, product_id: int) -> CartItem:
        """Get one cart item by user and product."""
        return (
            db.query(CartItem)
            .filter(CartItem.user_id == user_id, CartItem.product_id == product_id)
            .first()
        )

    @staticmethod
    def add_item(db: Session, user_id: int, product_id: int, quantity: int = 1) -> CartItem:
        """Add a product to the cart or increase its quantity."""
        item = CartRepository.get_item(db, user_id, product_id)
        if item:
            item.quantity += quantity
        else:
            item = CartItem(user_id=user_id, product_id=product_id, quantity=quantity)
            db.add(item)

        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def remove_item(db: Session, user_id: int, product_id: int) -> bool:
        """Remove one product from the cart."""
        item = CartRepository.get_item(db, user_id, product_id)
        if not item:
            return False

        db.delete(item)
        db.commit()
        return True

    @staticmethod
    def clear_cart(db: Session, user_id: int) -> None:
        """Remove all items from a user's cart."""
        db.query(CartItem).filter(CartItem.user_id == user_id).delete()
        db.commit()
