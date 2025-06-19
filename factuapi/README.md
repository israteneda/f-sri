# FactuAPI - Electronic Invoice System

A modern Django Rest Framework application for electronic invoice management with SRI (Ecuador Tax Authority) integration.

## 🚀 Features

- **Electronic Invoice Generation**: Complete invoice lifecycle management
- **SRI Integration**: Direct integration with Ecuador's tax authority system
- **PDF Generation**: Automatic PDF generation for invoices
- **Email Notifications**: Automated email notifications for invoice events
- **Multi-company Support**: Manage multiple issuing companies
- **Client Management**: Comprehensive client database
- **Product Catalog**: Product and service management
- **Audit Trail**: Complete audit trail for all operations
- **Real-time Monitoring**: Health checks and performance monitoring
- **Async Processing**: Background task processing with Celery
- **API Documentation**: Interactive API documentation with Swagger/OpenAPI

## 🛠 Technology Stack

- **Backend**: Django 4.2 + Django Rest Framework
- **Database**: PostgreSQL with Redis for caching
- **Task Queue**: Celery with Redis broker
- **Containerization**: Docker & Docker Compose
- **Web Server**: Nginx + Gunicorn
- **Monitoring**: Prometheus metrics, Sentry error tracking
- **Documentation**: drf-spectacular (Swagger/OpenAPI)

## 📋 Prerequisites

- Docker and Docker Compose
- Python 3.11+ (for local development)
- PostgreSQL (for local development)
- Redis (for local development)

## 🚀 Quick Start

### Using Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd factuapi
   ```

2. **Create environment file**
   ```bash
   cp .env.example .env
   # Edit .env file with your configuration
   ```

3. **Start the application**
   ```bash
   docker-compose up -d
   ```

4. **Run migrations**
   ```bash
   docker-compose exec web python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

6. **Load initial data**
   ```bash
   docker-compose exec web python manage.py loaddata fixtures/initial_data.json
   ```

### Local Development

1. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements/development.txt
   ```

3. **Set up database**
   ```bash
   createdb factuapi
   python manage.py migrate
   ```

4. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

5. **Run development server**
   ```bash
   python manage.py runserver
   ```

## 📚 API Documentation

- **Swagger UI**: http://localhost:8000/docs/
- **ReDoc**: http://localhost:8000/redoc/
- **OpenAPI Schema**: http://localhost:8000/api/schema/

## 🔧 Configuration

### Environment Variables

Key environment variables (see `.env.example` for complete list):

- `SECRET_KEY`: Django secret key
- `DEBUG`: Debug mode (True/False)
- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string
- `SRI_ENVIRONMENT`: SRI environment (1=Test, 2=Production)

### SRI Configuration

To configure SRI integration:

1. Set `SRI_ENVIRONMENT=1` for testing, `2` for production
2. Configure certificate paths and passwords
3. Set appropriate SRI endpoint URLs

## 🐳 Docker Commands

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f web

# Run management commands
docker-compose exec web python manage.py <command>

# Run tests
docker-compose exec web python manage.py test

# Shell access
docker-compose exec web python manage.py shell

# Database shell
docker-compose exec web python manage.py dbshell

# Stop all services
docker-compose down

# Production deployment
docker-compose -f docker-compose.prod.yml up -d
```

## 🧪 Testing

```bash
# Run all tests
python manage.py test

# Run with coverage
pytest --cov=apps --cov-report=html

# Run specific test
python manage.py test apps.invoices.tests.test_models
```

## 📊 Monitoring

- **Health Check**: http://localhost:8000/health/
- **Prometheus Metrics**: http://localhost:8000/metrics/
- **Django Admin**: http://localhost:8000/admin/
- **Silk Profiler** (dev only): http://localhost:8000/silk/

## 🔄 Development Workflow

1. **Code Quality**
   ```bash
   # Format code
   black .
   isort .
   
   # Lint code
   flake8
   pylint apps/
   
   # Type checking
   mypy apps/
   ```

2. **Database Migrations**
   ```bash
   # Create migrations
   python manage.py makemigrations
   
   # Apply migrations
   python manage.py migrate
   
   # Show migration status
   python manage.py showmigrations
   ```

3. **Static Files**
   ```bash
   # Collect static files
   python manage.py collectstatic
   ```

## 📱 API Endpoints

### Authentication
- `POST /api/v1/auth/login/` - User login
- `POST /api/v1/auth/refresh/` - Token refresh
- `POST /api/v1/auth/logout/` - User logout

### Companies
- `GET /api/v1/companies/` - List companies
- `POST /api/v1/companies/` - Create company
- `GET /api/v1/companies/{id}/` - Get company details

### Clients
- `GET /api/v1/clients/` - List clients
- `POST /api/v1/clients/` - Create client
- `GET /api/v1/clients/{id}/` - Get client details

### Products
- `GET /api/v1/products/` - List products
- `POST /api/v1/products/` - Create product
- `GET /api/v1/products/{id}/` - Get product details

### Invoices
- `GET /api/v1/invoices/` - List invoices
- `POST /api/v1/invoices/` - Create invoice
- `GET /api/v1/invoices/{id}/` - Get invoice details
- `POST /api/v1/invoices/{id}/send-sri/` - Send to SRI
- `GET /api/v1/invoices/{id}/pdf/` - Download PDF

## 🚀 Production Deployment

1. **Update environment variables**
   ```bash
   # Use production settings
   DJANGO_SETTINGS_MODULE=factuapi.settings.production
   DEBUG=False
   ```

2. **Use production docker-compose**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

3. **Set up SSL certificates**
   - Place SSL certificates in `docker/nginx/ssl/`
   - Update nginx configuration

4. **Configure monitoring**
   - Set up Sentry for error tracking
   - Configure log aggregation
   - Set up backup procedures

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and ensure code quality
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: Check the API documentation at `/docs/`
- **Issues**: Report issues on GitHub
- **Email**: support@factuapi.com

## 🔗 Related Links

- [Django Documentation](https://docs.djangoproject.com/)
- [Django Rest Framework](https://www.django-rest-framework.org/)
- [SRI Ecuador](https://www.sri.gob.ec/)
- [Celery Documentation](https://docs.celeryproject.org/)

---

**FactuAPI** - Making electronic invoicing simple and reliable for Ecuador 🇪🇨