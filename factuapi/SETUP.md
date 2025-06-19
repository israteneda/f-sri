# FactuAPI Setup Guide

This guide will help you set up the FactuAPI Django project locally or in production.

## Prerequisites

- **Docker & Docker Compose** (recommended)
- **Python 3.11+** (for local development)
- **PostgreSQL 15+** (if running locally without Docker)
- **Redis** (for caching and Celery)

## Quick Start with Docker

1. **Clone and Navigate**
```bash
cd factuapi
```

2. **Environment Setup**
```bash
cp .env.example .env
# Edit .env file with your configuration
```

3. **Build and Start**
```bash
make build
make up
```

4. **Run Migrations**
```bash
make migrate
```

5. **Create Superuser**
```bash
make createsuperuser
```

6. **Access the Application**
- API: http://localhost:8000/api/v1/
- Admin: http://localhost:8000/admin/
- API Documentation: http://localhost:8000/api/schema/swagger-ui/

## Local Development Setup

### 1. Python Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements/local.txt
```

### 2. Database Setup

**Option A: Using Docker for PostgreSQL only**
```bash
docker run --name factuapi-postgres \
  -e POSTGRES_DB=factuapi \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -p 5432:5432 \
  -d postgres:15
```

**Option B: Local PostgreSQL Installation**
```bash
# Ubuntu/Debian
sudo apt-get install postgresql postgresql-contrib

# macOS with Homebrew
brew install postgresql

# Create database
createdb factuapi
```

### 3. Redis Setup

**Option A: Using Docker**
```bash
docker run --name factuapi-redis -p 6379:6379 -d redis:7-alpine
```

**Option B: Local Installation**
```bash
# Ubuntu/Debian
sudo apt-get install redis-server

# macOS with Homebrew
brew install redis
```

### 4. Django Setup

```bash
# Set environment variables
export DJANGO_SETTINGS_MODULE=config.settings.local
export DATABASE_URL=postgresql://postgres:postgres@localhost:5432/factuapi

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

## Environment Variables

### Required Variables

```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:pass@host:port/dbname
```

### Optional Variables

```env
# Debug mode (default: False)
DEBUG=True

# Allowed hosts (comma-separated)
ALLOWED_HOSTS=localhost,127.0.0.1

# Redis URL for caching and Celery
REDIS_URL=redis://localhost:6379/0

# JWT secret key (defaults to SECRET_KEY)
JWT_SECRET_KEY=your-jwt-secret

# Email configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# SRI Configuration for Ecuador
SRI_AMBIENTE=1  # 1: Testing, 2: Production
```

## Development Workflow

### Code Quality

```bash
# Format code
make format

# Run linting
make lint

# Install pre-commit hooks
pre-commit install
```

### Testing

```bash
# Run all tests
make test

# Run with coverage
make test-coverage

# Run specific test
python manage.py test apps.clients.tests.ClientModelTestCase
```

### Database Operations

```bash
# Create migrations
make makemigrations

# Apply migrations
make migrate

# Reset database (Docker)
make reset-db
```

## Production Deployment

### 1. Environment Configuration

Create production `.env` file:
```env
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:password@host:port/dbname
REDIS_URL=redis://redis:6379/0

# Email configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.yourdomain.com

# Optional: AWS S3 for file storage
USE_S3=True
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
AWS_STORAGE_BUCKET_NAME=your-bucket

# Optional: Sentry for error tracking
SENTRY_DSN=https://your-sentry-dsn
```

### 2. Docker Production Deployment

```bash
# Build production images
make prod-build

# Start production services
make prod-up

# Run migrations
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate

# Collect static files
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput

# Create superuser
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
```

### 3. SSL Configuration

1. Place SSL certificates in `docker/nginx/ssl/`
2. Uncomment HTTPS server block in `docker/nginx/nginx.conf`
3. Update certificate paths
4. Restart nginx

## Common Issues

### Database Connection Issues

1. **PostgreSQL not running**: Start PostgreSQL service
2. **Permission denied**: Check database user permissions
3. **Database doesn't exist**: Create database manually

### Redis Connection Issues

1. **Redis not running**: Start Redis service
2. **Connection refused**: Check Redis configuration and firewall

### Migration Issues

1. **Migration conflicts**: Run `python manage.py showmigrations` to check status
2. **Fake migrations**: Use `--fake` flag if needed
3. **Reset migrations**: Delete migration files and run `makemigrations`

## API Usage Examples

### Authentication

```bash
# Register user
curl -X POST http://localhost:8000/api/v1/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "email": "test@example.com", "password": "testpass123", "password_confirm": "testpass123"}'

# Login
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "testpass123"}'
```

### Clients

```bash
# Create client (requires authentication)
curl -X POST http://localhost:8000/api/v1/clients/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"identification_type": 1, "identification": "1234567890", "business_name": "Test Client", "address": "Test Address"}'

# List clients
curl -X GET http://localhost:8000/api/v1/clients/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Support

For issues and questions:
1. Check the logs: `make logs`
2. Review this documentation
3. Check Django and DRF documentation
4. Open an issue in the project repository