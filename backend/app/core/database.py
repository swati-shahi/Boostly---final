from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# SQLite requires 'check_same_thread: False' to allow multi-threaded FastAPI requests; Postgres does not
connect_args = {"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    settings.DATABASE_URL, 
    connect_args=connect_args
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """
    FastAPI dependency yielding isolated database sessions per request.
    Ensures safe session closure even upon unexpected route errors.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()