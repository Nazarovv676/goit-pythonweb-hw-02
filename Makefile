# Makefile
.PHONY: help build up down logs ps restart clean test healthcheck

help:
	@echo "Available targets:"
	@echo "  make build       - Build Docker images"
	@echo "  make up          - Start services in detached mode"
	@echo "  make down        - Stop and remove services"
	@echo "  make logs        - Show logs from all services"
	@echo "  make ps          - Show service status"
	@echo "  make restart     - Restart all services"
	@echo "  make clean       - Stop services and remove volumes"
	@echo "  make test        - Run healthcheck verification"
	@echo "  make healthcheck - Run healthcheck script"

build:
	docker compose build

up:
	docker compose up -d --build

down:
	docker compose down

logs:
	docker compose logs -f

ps:
	docker compose ps

restart:
	docker compose restart

clean:
	docker compose down -v

test:
	@echo "Checking service health..."
	@docker compose ps
	@echo ""
	@echo "Testing HTTP endpoint..."
	@curl -f http://localhost:8000/ > /dev/null && echo "✓ HTTP endpoint OK" || echo "✗ HTTP endpoint failed"
	@echo ""
	@echo "Testing healthcheck endpoint..."
	@curl -f http://localhost:8000/healthchecker > /dev/null && echo "✓ Healthcheck endpoint OK" || echo "✗ Healthcheck endpoint failed"

healthcheck:
	docker compose exec app python /app/docker/healthcheck.py

