#!/usr/bin/env python3
# docker/wait_for_db.py
import os
import sys
import time
from urllib.parse import urlparse

def wait_for_db(max_retries=30, retry_delay=2):
    """Wait for PostgreSQL database to be ready."""
    DATABASE_URL = os.getenv("DATABASE_URL", "")
    
    if DATABASE_URL:
        # Parse DATABASE_URL: postgresql+psycopg2://user:pass@host:port/dbname
        url = DATABASE_URL.replace("postgresql+psycopg2://", "postgresql://")
        parsed = urlparse(url)
        host = parsed.hostname
        port = parsed.port or 5432
        user = parsed.username
        password = parsed.password
        dbname = parsed.path[1:] if parsed.path else None
    else:
        # Fallback to individual env vars
        host = os.getenv("DB_HOST", "db")
        port = int(os.getenv("DB_PORT", "5432"))
        user = os.getenv("POSTGRES_USER", "postgres")
        password = os.getenv("POSTGRES_PASSWORD", "567234")
        dbname = os.getenv("POSTGRES_DB", "hw02")
    
    import psycopg2
    
    for attempt in range(1, max_retries + 1):
        try:
            conn = psycopg2.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                dbname=dbname,
                connect_timeout=5
            )
            conn.close()
            print(f"PostgreSQL is ready!")
            return True
        except Exception as e:
            if attempt < max_retries:
                print(f"Attempt {attempt}/{max_retries}: PostgreSQL not ready, waiting... ({e})")
                time.sleep(retry_delay)
            else:
                print(f"ERROR: PostgreSQL did not become ready after {max_retries} attempts")
                return False
    
    return False

if __name__ == "__main__":
    success = wait_for_db()
    sys.exit(0 if success else 1)

