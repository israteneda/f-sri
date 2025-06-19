.PHONY: help build up down logs shell test clean install lint format check migrate superuser

# Default target
help:
	@echo "Available commands:"
	@echo "  build       - Build Docker images"
	@echo "  up          - Start all services"
	@echo "  down        - Stop all services"
	@echo "  logs        - View logs"
	@echo "  shell       - Access Django shell"
	@echo "  test        - Run tests"
	@echo "  clean       - Clean up Docker resources"
	@echo "  install     - Install dependencies"
	@echo "  lint        - Run linting tools"
	@echo "  format      - Format code"
	@echo "  check       - Run all checks"
	@echo "  migrate     - Run database migrations"
	@echo "  superuser   - Create superuser"

# Docker commands
build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f web

shell:
	docker-compose exec web python manage.py shell

dbshell:
	docker-compose exec web python manage.py dbshell

# Development commands
install:
	pip install -r requirements/development.txt

test:
	docker-compose exec web python manage.py test

test-local:
	pytest

coverage:
	docker-compose exec web pytest --cov=apps --cov-report=html

# Code quality
lint:
	flake8 apps/
	pylint apps/
	bandit -r apps/

format:
	black apps/
	isort apps/

type-check:
	mypy apps/

check: format lint type-check test

# Database commands
migrate:
	docker-compose exec web python manage.py migrate

makemigrations:
	docker-compose exec web python manage.py makemigrations

superuser:
	docker-compose exec web python manage.py createsuperuser

# Production commands
prod-up:
	docker-compose -f docker-compose.prod.yml up -d

prod-down:
	docker-compose -f docker-compose.prod.yml down

prod-build:
	docker-compose -f docker-compose.prod.yml build

# Utility commands
clean:
	docker-compose down -v --remove-orphans
	docker system prune -f

reset-db:
	docker-compose exec web python manage.py flush --noinput
	docker-compose exec web python manage.py migrate
	docker-compose exec web python manage.py loaddata fixtures/initial_data.json

collectstatic:
	docker-compose exec web python manage.py collectstatic --noinput

# Local development (without Docker)
local-install:
	python -m venv venv
	. venv/bin/activate && pip install -r requirements/development.txt

local-migrate:
	python manage.py migrate

local-run:
	python manage.py runserver

local-test:
	python manage.py test

# Backup and restore
backup-db:
	docker-compose exec db pg_dump -U factuapi factuapi > backup_$(shell date +%Y%m%d_%H%M%S).sql

restore-db:
	docker-compose exec -T db psql -U factuapi factuapi < $(FILE)

# Monitoring
htop:
	docker-compose exec web htop

logs-web:
	docker-compose logs -f web

logs-db:
	docker-compose logs -f db

logs-celery:
	docker-compose logs -f celery

logs-redis:
	docker-compose logs -f redis