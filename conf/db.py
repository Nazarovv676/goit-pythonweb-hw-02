import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Read DATABASE_URL from environment, or build from individual components
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    # Build from individual environment variables with defaults
    db_host = os.getenv("DB_HOST", "db")  # Default to compose service name
    db_port = os.getenv("DB_PORT", "5432")
    db_user = os.getenv("POSTGRES_USER", "postgres")
    db_password = os.getenv("POSTGRES_PASSWORD", "567234")
    db_name = os.getenv("POSTGRES_DB", "hw02")
    DATABASE_URL = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

SQLALCHEMY_DATABASE_URL = DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True, max_overflow=5)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
