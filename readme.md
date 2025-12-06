# FastAPI Docker Deployment

This project containerizes a FastAPI application with PostgreSQL using Docker Compose.

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2
- Git

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/GoIT-Python-Web/FullStack-Web-Development-hw2.git
cd FullStack-Web-Development-hw2
```

### 2. Configure environment

```bash
cp .env.example .env
```

Edit `.env` if needed (defaults should work for local development).

### 3. Build and start services

```bash
docker compose up -d --build
```

### 4. Verify deployment

1. **Check service status:**
   ```bash
   docker compose ps
   ```
   Both `app` and `db` services should show `healthy` status.

2. **Test HTTP endpoint:**
   ```bash
   curl -f http://localhost:8000/
   ```
   Should return HTML with "Welcome to FastAPI!" or similar content.

3. **Open in browser:**
   Navigate to http://localhost:8000/
   - You should see the FastAPI welcome page
   - Click "Перевірити БД" button
   - Should show success message if database connection works

4. **Test healthcheck endpoint:**
   ```bash
   curl http://localhost:8000/healthchecker
   ```
   Should return: `{"message": "Welcome to FastAPI!"}`

## Troubleshooting

### Services not starting

**Problem:** `docker compose ps` shows services as unhealthy or restarting.

**Solutions:**
- Check logs: `docker compose logs app` and `docker compose logs db`
- Verify `.env` file exists and contains correct values
- Ensure port 8000 is not already in use: `lsof -i :8000`
- Check PostgreSQL logs: `docker compose logs db | tail -50`

### Database connection errors

**Problem:** "Error connecting to the database" or "Database is not configured correctly"

**Solutions:**
- Verify `DATABASE_URL` in docker-compose.yaml uses service name `db` (not `localhost`)
- Check that `conf/db.py` reads from environment variables
- Ensure database service is healthy: `docker compose ps db`
- Test database connection manually:
  ```bash
  docker compose exec db psql -U postgres -d hw02 -c "SELECT 1;"
  ```

### Port already in use

**Problem:** `Error: bind: address already in use`

**Solution:**
- Change `APP_PORT` in `.env` to a different port (e.g., 8001)
- Update docker-compose.yaml ports mapping accordingly

### Container permissions issues

**Problem:** Permission denied errors in container

**Solution:**
- Ensure entrypoint.sh is executable: `chmod +x docker/entrypoint.sh`
- Rebuild: `docker compose build --no-cache app`

## Useful Commands

### View logs

```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f app
docker compose logs -f db
```

### Stop services

```bash
docker compose down
```

### Stop and remove volumes (clean slate)

```bash
docker compose down -v
```

### Rebuild after code changes

```bash
docker compose up -d --build app
```

### Execute commands in container

```bash
# Access app container shell
docker compose exec app bash

# Access database
docker compose exec db psql -U postgres -d hw02
```

### Check health status

```bash
docker compose ps
docker compose exec app python docker/healthcheck.py
```

## Architecture

- **app**: FastAPI application (Python 3.10)
  - Runs as non-root user (`appuser`)
  - Waits for database readiness before starting
  - Healthcheck verifies HTTP and database connectivity

- **db**: PostgreSQL 15
  - Persistent data in Docker volume
  - Healthcheck via `pg_isready`

## Environment Variables

See `.env.example` for available configuration options:

- `POSTGRES_DB`: Database name (default: `hw02`)
- `POSTGRES_USER`: Database user (default: `postgres`)
- `POSTGRES_PASSWORD`: Database password (default: `567234`)
- `APP_HOST`: Application bind address (default: `0.0.0.0`)
- `APP_PORT`: Application port (default: `8000`)

The `DATABASE_URL` is automatically constructed in docker-compose.yaml using the service name `db` as the host.

## Verification Checklist

- [ ] `docker compose ps` shows both services as healthy
- [ ] `curl http://localhost:8000/` returns 200 OK
- [ ] Browser shows FastAPI welcome page
- [ ] "Перевірити БД" button returns success
- [ ] No `localhost` references in application database config
- [ ] Database connection uses service name `db`
