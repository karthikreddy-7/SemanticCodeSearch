from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from coderag.config.settings import SQLITE_DB_PATH
from coderag.database.relational.models import Base

DATABASE_URL = f"sqlite:///{SQLITE_DB_PATH}"

# `check_same_thread=False` allows using sessions across threads (useful for indexers)
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}, echo=False
)

# Scoped session ensures thread-local isolation
SessionLocal = scoped_session(sessionmaker(bind=engine, autoflush=False, autocommit=False))


def init_db():
    """Create all tables based on SQLAlchemy models."""
    Base.metadata.create_all(bind=engine)
    print(f"✅ SQLite DB initialized at: {SQLITE_DB_PATH}")


def get_db():
    """
    Dependency-style generator for safely managing sessions.
    Example:
        with get_db() as db:
            repos = db.query(Repository).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
