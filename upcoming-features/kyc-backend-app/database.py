from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from config import get_settings, get_database_url

# Don't create engine at import time - create it when needed
_engine = None
_SessionLocal = None

def get_engine():
    """Get or create the database engine"""
    global _engine
    if _engine is None:
        settings = get_settings()
        database_url = get_database_url()
        
        if not database_url:
            raise ValueError("Database URL is empty. Please check your environment configuration.")
        
        if settings.ENV == "local":
            _engine = create_engine(
                database_url,
                connect_args={"check_same_thread": False}
            )
        else:
            # For AWS RDS (PostgreSQL)
            _engine = create_engine(
                database_url,
                pool_pre_ping=True,  # Enable connection health checks
                pool_size=5,  # Adjust based on your needs
                max_overflow=10
            )
    return _engine

def get_session_local():
    """Get or create the session local"""
    global _SessionLocal
    if _SessionLocal is None:
        engine = get_engine()
        _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return _SessionLocal

def init_db():
    """Initialize the database by creating all tables"""
    engine = get_engine()
    Base.metadata.create_all(bind=engine)

def get_db():
    """Get database session"""
    SessionLocal = get_session_local()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 