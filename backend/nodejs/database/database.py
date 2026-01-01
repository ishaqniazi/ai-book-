from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Generator
import os
from contextlib import contextmanager

# Database configuration
DATABASE_URL = os.getenv(
    "NEON_DATABASE_URL",
    "postgresql://neondb_owner:npg_wt0oFVnIXf8b@ep-aged-rice-ab3h775b-pooler.eu-west-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
)

# Create engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=300,    # Recycle connections after 5 minutes
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for models
Base = declarative_base()

# Dependency to get DB session
def get_db() -> Generator:
    """
    Dependency for FastAPI to get database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Context manager for database sessions
@contextmanager
def get_db_session():
    """
    Context manager for database sessions outside of FastAPI
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Function to initialize the database
def init_db():
    """
    Initialize the database by creating all tables
    """
    from .models import Base
    Base.metadata.create_all(bind=engine)

# Function to test the database connection
def test_connection():
    """
    Test the database connection
    """
    try:
        with get_db_session() as db:
            # Try to execute a simple query
            result = db.execute("SELECT 1")
            return result.fetchone() is not None
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False