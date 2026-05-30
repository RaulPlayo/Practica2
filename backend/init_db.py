"""
Inicializa la base de datos con usuarios y productos de prueba.
Ejecutar desde backend: python init_db.py
"""

from app.core.database import SessionLocal, init_db
from app.core.security import hash_password
from app.models import Product
from app.repositories import ProductRepository, UserRepository


def upsert_user(db, username: str, password: str, role: str):
    existing_user = UserRepository.get_by_username(db, username)
    if existing_user:
        UserRepository.update(
            db,
            existing_user.id,
            hashed_password=hash_password(password),
            role=role,
        )
        return "actualizado"

    UserRepository.create(
        db,
        username=username,
        hashed_password=hash_password(password),
        role=role,
    )
    return "creado"


def create_product_if_missing(db, nombre: str, descripcion: str, precio: float, stock: int):
    existing_product = db.query(Product).filter(Product.nombre == nombre).first()
    if existing_product:
        return "ya existe"

    ProductRepository.create(
        db,
        nombre=nombre,
        descripcion=descripcion,
        precio=precio,
        stock=stock,
    )
    return "creado"


def init_database_with_data():
    print("1. Creando tablas y aplicando migraciones...")
    init_db()
    print("   OK")

    db = SessionLocal()

    try:
        print("\n2. Creando usuarios de prueba...")
        print(f"   admin/admin123: {upsert_user(db, 'admin', 'admin123', 'admin')}")
        print(f"   usuario/usuario123: {upsert_user(db, 'usuario', 'usuario123', 'usuario')}")

        print("\n3. Creando productos de prueba...")
        products_data = [
            ("Laptop Pro", "Laptop de alta performance para profesionales", 1299.99, 5),
            ("Mouse Inalambrico", "Mouse ergonomico con bateria de larga duracion", 29.99, 50),
            ("Teclado Mecanico", "Teclado mecanico RGB para gaming", 149.99, 15),
            ("Monitor 4K", "Monitor 4K de 32 pulgadas", 499.99, 8),
            ("Webcam HD", "Camara web 1080p con microfono integrado", 79.99, 30),
            ("Auriculares Bluetooth", "Auriculares inalambricos con cancelacion de ruido", 199.99, 20),
            ("Cable USB-C", "Cable USB-C de carga rapida 100W", 19.99, 100),
            ("Hub USB", "Hub USB 3.0 con 7 puertos", 49.99, 25),
        ]

        for nombre, descripcion, precio, stock in products_data:
            status = create_product_if_missing(db, nombre, descripcion, precio, stock)
            print(f"   {nombre}: {status}")

        print("\nBase de datos inicializada correctamente.")
        print("Credenciales: admin/admin123 y usuario/usuario123")

    except Exception as exc:
        print(f"\nError inicializando la base de datos: {exc}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    init_database_with_data()
