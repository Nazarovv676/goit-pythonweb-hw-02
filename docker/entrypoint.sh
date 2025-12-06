#!/bin/bash
# docker/entrypoint.sh
set -e

APP_HOST=${APP_HOST:-0.0.0.0}
APP_PORT=${APP_PORT:-8000}
APP_MODULE=${APP_MODULE:-main:app}

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to be ready..."
python /app/docker/wait_for_db.py || exit 1

# Start uvicorn
echo "Starting uvicorn on ${APP_HOST}:${APP_PORT}..."
exec uvicorn ${APP_MODULE} --host ${APP_HOST} --port ${APP_PORT} --log-level info

