import os
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker, declarative_base

# Database URL (SQLite)
DATABASE_URL = "sqlite:///./practica2.db"

# Create engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # Required for SQLite
    echo=False  # Set to True for SQL debugging
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for models
Base = declarative_base()


def get_db():
    """Dependency to get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables."""
    Base.metadata.create_all(bind=engine)
    migrate_db()


def migrate_db():
    """Apply tiny SQLite migrations needed by the current models."""
    inspector = inspect(engine)
    if "products" not in inspector.get_table_names():
        return

    product_columns = {column["name"] for column in inspector.get_columns("products")}
    with engine.begin() as connection:
        if "imagen" not in product_columns:
            connection.execute(text("ALTER TABLE products ADD COLUMN imagen VARCHAR"))
        if "estado" not in product_columns:
            connection.execute(text("ALTER TABLE products ADD COLUMN estado VARCHAR NOT NULL DEFAULT 'activo'"))
