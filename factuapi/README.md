# FactuAPI - Django Electronic Invoicing System

A Django Rest Framework based electronic invoicing system for Ecuador with SRI integration, containerized with Docker.

## Features

- 🚀 Django Rest Framework API
- 🐳 Docker containerization with multi-stage builds
- 🔐 JWT Authentication
- 📊 PostgreSQL database
- 📝 Automatic API documentation with drf-spectacular
- 🧪 Comprehensive testing setup
- 🔧 Code formatting with Black and isort
- 📋 Linting with flake8 and mypy
- 🌍 CORS configuration
- 🏗️ Production-ready configuration
- 📄 Electronic invoice generation and PDF support
- 🏢 SRI (Ecuador Tax System) integration ready

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.11+ (for local development)

### Using Docker (Recommended)

1. Clone and setup:
```bash
git clone <your-repo>
cd factuapi
cp .env.example .env
```

2. Build and run:
```bash
docker-compose up --build
```

3. Run migrations and create superuser:
```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

4. Access the application:
- API: http://localhost:8000/api/v1/
- Admin: http://localhost:8000/admin/
- API Docs: http://localhost:8000/api/schema/swagger-ui/

### Local Development

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

2. Install dependencies:
```bash
pip install -r requirements/local.txt
```

3. Setup database:
```bash
python manage.py migrate
python manage.py createsuperuser
```

4. Run development server:
```bash
python manage.py runserver
```

## Project Structure

```
factuapi/
├── apps/                          # Django applications
│   ├── authentication/           # User authentication
│   ├── clients/                   # Client management
│   ├── invoices/                  # Invoice management
│   ├── products/                  # Product catalog
│   └── core/                      # Shared utilities
├── config/                        # Django settings
├── requirements/                  # Python dependencies
├── docker/                        # Docker configurations
├── docs/                          # Documentation
└── tests/                         # Test files
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/login/` - User login
- `POST /api/v1/auth/refresh/` - Refresh JWT token
- `POST /api/v1/auth/register/` - User registration

### Clients
- `GET /api/v1/clients/` - List clients
- `POST /api/v1/clients/` - Create client
- `GET /api/v1/clients/{id}/` - Get client details
- `PUT /api/v1/clients/{id}/` - Update client
- `DELETE /api/v1/clients/{id}/` - Delete client

### Invoices
- `GET /api/v1/invoices/` - List invoices
- `POST /api/v1/invoices/` - Create invoice
- `GET /api/v1/invoices/{id}/` - Get invoice details
- `GET /api/v1/invoices/{id}/pdf/` - Download invoice PDF

### Products
- `GET /api/v1/products/` - List products
- `POST /api/v1/products/` - Create product

## Testing

Run tests with coverage:
```bash
# Using Docker
docker-compose exec web python manage.py test

# Local
python manage.py test
coverage run --source='.' manage.py test
coverage report
```

## Code Quality

Format code:
```bash
black .
isort .
```

Lint code:
```bash
flake8
mypy .
```

## Environment Variables

Copy `.env.example` to `.env` and configure:

```env
# Django
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=postgresql://user:password@db:5432/factuapi

# JWT
JWT_SECRET_KEY=your-jwt-secret

# Email (optional)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

## Production Deployment

1. Set environment variables
2. Use production docker-compose:
```bash
docker-compose -f docker-compose.prod.yml up --build
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## License

MIT License - see LICENSE file for details.