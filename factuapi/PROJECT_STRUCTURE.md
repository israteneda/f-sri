# FactuAPI - Project Structure

This document provides an overview of the complete Django Rest Framework project template that has been created.

## 📁 Project Structure

```
factuapi/
├── 📄 manage.py                      # Django management script
├── 📄 README.md                      # Main documentation
├── 📄 .env.example                   # Environment variables template
├── 📄 .gitignore                     # Git ignore rules
├── 📄 Makefile                       # Development automation
├── 📄 pytest.ini                     # Pytest configuration
├── 📄 pyproject.toml                 # Python project configuration
├── 📄 PROJECT_STRUCTURE.md           # This file
│
├── 📂 docker/                        # Docker configuration
│   ├── 📄 Dockerfile                 # Multi-stage Docker build
│   ├── 📂 nginx/                     # Nginx configuration
│   │   ├── 📄 nginx.conf             # Development nginx config
│   │   └── 📄 nginx.prod.conf        # Production nginx config
│   └── 📂 postgres/                  # PostgreSQL configuration
│       └── 📄 init.sql               # Database initialization
│
├── 📂 requirements/                  # Python dependencies
│   ├── 📄 base.txt                   # Base requirements
│   ├── 📄 development.txt            # Development requirements
│   └── 📄 production.txt             # Production requirements
│
├── 📂 scripts/                       # Utility scripts
│   └── 📄 setup.sh                   # Quick setup script
│
├── 📂 factuapi/                      # Main Django project
│   ├── 📄 __init__.py                # Project package
│   ├── 📄 urls.py                    # Main URL configuration
│   ├── 📄 wsgi.py                    # WSGI configuration
│   ├── 📄 asgi.py                    # ASGI configuration
│   ├── 📄 celery.py                  # Celery configuration
│   └── 📂 settings/                  # Settings package
│       ├── 📄 __init__.py            # Settings package
│       ├── 📄 base.py                # Base settings
│       ├── 📄 development.py         # Development settings
│       ├── 📄 production.py          # Production settings
│       └── 📄 testing.py             # Testing settings
│
├── 📂 apps/                          # Django applications
│   ├── 📄 __init__.py                # Apps package
│   └── 📂 core/                      # Core application
│       ├── 📄 __init__.py            # App package
│       ├── 📄 apps.py                # App configuration
│       ├── 📄 models.py              # Base models
│       ├── 📄 views.py               # Core views
│       ├── 📄 urls.py                # URL patterns
│       ├── 📄 admin.py               # Admin configuration
│       └── 📄 exceptions.py          # Custom exceptions
│
├── 📄 docker-compose.yml             # Development environment
└── 📄 docker-compose.prod.yml        # Production environment
```

## 🚀 Key Features Implemented

### 🐳 Docker Configuration
- **Multi-stage Dockerfile**: Optimized for both development and production
- **Docker Compose**: Complete development environment with PostgreSQL, Redis, Celery
- **Nginx**: Production-ready reverse proxy with SSL support
- **Health Checks**: Container health monitoring

### ⚙️ Django Settings
- **Modular Settings**: Separate configurations for development, production, and testing
- **Environment Variables**: Secure configuration management
- **Security**: Production-ready security settings
- **Logging**: Structured logging with different levels per environment

### 📦 Dependencies Management
- **Requirements Structure**: Separate files for different environments
- **Modern Libraries**: Latest versions of Django, DRF, and essential packages
- **Development Tools**: Code quality, testing, and debugging tools

### 🏗️ Project Architecture
- **Django Rest Framework**: Full API framework setup
- **JWT Authentication**: Token-based authentication
- **API Documentation**: Swagger/OpenAPI integration
- **CORS**: Cross-origin resource sharing configuration
- **Celery**: Asynchronous task processing
- **Redis**: Caching and message broker

### 🛠️ Development Tools
- **Code Quality**: Black, isort, flake8, pylint, bandit
- **Testing**: Pytest with coverage reporting
- **Type Checking**: MyPy configuration
- **Pre-commit**: Code quality enforcement
- **Makefile**: Common development tasks automation

### 🔧 Core Features
- **Base Models**: Abstract models with timestamps, UUID, and audit trail
- **Custom Exception Handling**: Consistent API error responses
- **Health Checks**: System monitoring endpoints
- **Admin Interface**: Django admin configuration
- **Internationalization**: Spanish (Ecuador) localization

## 📊 Database Models

### Core Models Included:
- **IdentificationType**: Document types (Cédula, RUC, Passport, etc.)
- **Country**: Country catalog
- **Province**: State/province catalog
- **City**: City catalog
- **Currency**: Currency management
- **TaxType**: Tax type definitions (IVA, ICE, etc.)

### Planned App Structure:
- **authentication**: User management and JWT authentication
- **companies**: Issuing company management
- **clients**: Customer database
- **products**: Product and service catalog
- **invoices**: Electronic invoice processing
- **notifications**: Email and system notifications
- **reports**: Business intelligence and reporting

## 🚀 Getting Started

### Quick Start (Recommended)
```bash
cd factuapi
./scripts/setup.sh
```

### Manual Setup
```bash
# Copy environment file
cp .env.example .env

# Start services
make up

# Run migrations
make migrate

# Create superuser
make superuser
```

## 📚 API Endpoints

### Planned API Structure:
- `GET /` - API root with endpoint discovery
- `GET /health/` - Health check endpoint
- `GET /docs/` - Swagger API documentation
- `POST /api/v1/auth/login/` - User authentication
- `GET /api/v1/companies/` - Company management
- `GET /api/v1/clients/` - Client management
- `GET /api/v1/products/` - Product catalog
- `GET /api/v1/invoices/` - Invoice management

## 🔧 Environment Configuration

### Key Environment Variables:
```bash
# Django
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=postgresql://factuapi:factuapi123@db:5432/factuapi

# Redis
REDIS_URL=redis://redis:6379/1
CELERY_BROKER_URL=redis://redis:6379/0

# SRI (Ecuador Tax Authority)
SRI_ENVIRONMENT=1  # 1=Test, 2=Production
SRI_BASE_URL=https://celcer.sri.gob.ec/comprobantes-electronicos-ws/
```

## 🧪 Testing

### Test Structure:
- **Unit Tests**: Model and utility testing
- **API Tests**: Endpoint testing
- **Integration Tests**: End-to-end functionality
- **SRI Tests**: Tax authority integration testing

### Running Tests:
```bash
# All tests
make test

# With coverage
make coverage

# Specific tests
pytest apps/core/tests/
```

## 📈 Production Deployment

### Production Features:
- **SSL/TLS**: HTTPS with security headers
- **Static File Serving**: Nginx static file serving
- **Database Pooling**: Connection pooling for performance
- **Caching**: Redis caching for improved performance
- **Error Tracking**: Sentry integration
- **Monitoring**: Prometheus metrics
- **Logging**: Structured JSON logging

### Deployment Commands:
```bash
# Production build
make prod-build

# Start production
make prod-up

# SSL certificates
# Place certificates in docker/nginx/ssl/
```

## 🔄 Development Workflow

### Code Quality Workflow:
```bash
# Format code
make format

# Lint code
make lint

# Type check
make type-check

# Run all checks
make check
```

### Database Workflow:
```bash
# Create migrations
make makemigrations

# Apply migrations
make migrate

# Reset database
make reset-db
```

## 🤝 Contributing

This template provides a solid foundation for electronic invoice management systems. The structure is designed to be:

- **Scalable**: Modular app architecture
- **Maintainable**: Clean code practices and documentation
- **Secure**: Production-ready security configuration
- **Testable**: Comprehensive testing setup
- **Deployable**: Docker-based deployment strategy

## 📝 Next Steps

1. **Implement Authentication App**: User management with JWT
2. **Create Company Management**: Multi-tenant company setup
3. **Build Client Database**: Customer management system
4. **Develop Product Catalog**: Product and service management
5. **Implement Invoice Engine**: Electronic invoice generation
6. **SRI Integration**: Ecuador tax authority integration
7. **PDF Generation**: Invoice PDF creation
8. **Email Notifications**: Automated email system
9. **Reporting System**: Business intelligence dashboard
10. **API Rate Limiting**: Production-ready API protection

This template serves as a robust starting point for building a comprehensive electronic invoice system with modern Django best practices and production-ready configuration.

---

**FactuAPI** - Professional electronic invoicing for Ecuador 🇪🇨