from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://remedylab_backbone:remedylab123@localhost/remedylab_db",
)

# ✅ Add pool_pre_ping to refresh stale connections
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Detects dead connections
    pool_size=5,  # Default pool size
    max_overflow=10,  # Extra connections beyond pool_size
    pool_timeout=30,  # Wait before throwing connection error
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
