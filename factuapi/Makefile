.PHONY: help build up down logs shell test clean migrate format lint

# Default target
help:
	@echo "Available commands:"
	@echo "  build       - Build Docker images"
	@echo "  up          - Start development environment"
	@echo "  down        - Stop development environment"
	@echo "  logs        - View logs"
	@echo "  shell       - Access Django shell"
	@echo "  test        - Run tests"
	@echo "  clean       - Clean up Docker resources"
	@echo "  migrate     - Run Django migrations"
	@echo "  makemigrations - Create Django migrations"
	@echo "  createsuperuser - Create Django superuser"
	@echo "  format      - Format code with Black and isort"
	@echo "  lint        - Run linting tools"
	@echo "  install     - Install local dependencies"

# Docker commands
build:
	docker-compose build

up:
	docker-compose up -d
	@echo "Application is running at http://localhost:8000"

down:
	docker-compose down

logs:
	docker-compose logs -f

shell:
	docker-compose exec web python manage.py shell

# Django commands
migrate:
	docker-compose exec web python manage.py migrate

makemigrations:
	docker-compose exec web python manage.py makemigrations

createsuperuser:
	docker-compose exec web python manage.py createsuperuser

collectstatic:
	docker-compose exec web python manage.py collectstatic --noinput

# Testing
test:
	docker-compose exec web python manage.py test

test-coverage:
	docker-compose exec web coverage run --source='.' manage.py test
	docker-compose exec web coverage report
	docker-compose exec web coverage html

# Code quality
format:
	black .
	isort .

lint:
	flake8
	mypy .
	black --check .
	isort --check-only .

# Local development
install:
	pip install -r requirements/local.txt

local-migrate:
	python manage.py migrate

local-test:
	python manage.py test

local-run:
	python manage.py runserver

# Production
prod-build:
	docker-compose -f docker-compose.prod.yml build

prod-up:
	docker-compose -f docker-compose.prod.yml up -d

prod-down:
	docker-compose -f docker-compose.prod.yml down

# Cleanup
clean:
	docker-compose down -v
	docker system prune -f
	docker volume prune -f

# Database
reset-db:
	docker-compose down -v
	docker-compose up -d db
	@echo "Waiting for database to be ready..."
	@sleep 5
	docker-compose up -d web
	docker-compose exec web python manage.py migrate
	docker-compose exec web python manage.py createsuperuser --noinput --email admin@factuapi.com --username admin || true