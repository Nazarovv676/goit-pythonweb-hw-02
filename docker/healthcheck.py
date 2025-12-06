#!/usr/bin/env python3
# docker/healthcheck.py
import os
import sys
import urllib.request
import urllib.error
from urllib.parse import urlparse

APP_PORT = int(os.getenv("APP_PORT", "8000"))

# Test HTTP endpoint
try:
    response = urllib.request.urlopen(f"http://localhost:{APP_PORT}/", timeout=5)
    if response.getcode() != 200:
        print(f"HTTP healthcheck failed: status {response.getcode()}")
        sys.exit(1)
    content = response.read().decode('utf-8')
    if "Welcome to FastAPI" not in content and "FastAPI" not in content:
        print("HTTP healthcheck failed: unexpected content")
        sys.exit(1)
except Exception as e:
    print(f"HTTP healthcheck failed: {e}")
    sys.exit(1)

# Test database connection
try:
    import psycopg2
    
    DATABASE_URL = os.getenv("DATABASE_URL", "")
    if DATABASE_URL:
        # Parse DATABASE_URL: postgresql+psycopg2://user:pass@host:port/dbname
        url = DATABASE_URL.replace("postgresql+psycopg2://", "postgresql://")
        parsed = urlparse(url)
        conn = psycopg2.connect(
            host=parsed.hostname,
            port=parsed.port or 5432,
            user=parsed.username,
            password=parsed.password,
            dbname=parsed.path[1:] if parsed.path else None
        )
    else:
        # Fallback to individual env vars
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "db"),
            port=int(os.getenv("DB_PORT", "5432")),
            user=os.getenv("POSTGRES_USER", "postgres"),
            password=os.getenv("POSTGRES_PASSWORD", "567234"),
            dbname=os.getenv("POSTGRES_DB", "hw02")
        )
    
    cursor = conn.cursor()
    cursor.execute("SELECT 1")
    cursor.fetchone()
    cursor.close()
    conn.close()
except Exception as e:
    print(f"Database healthcheck failed: {e}")
    sys.exit(1)

print("Healthcheck passed")
sys.exit(0)

