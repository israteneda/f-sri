#!/bin/bash

# FactuAPI Setup Script
# This script helps you get started with the FactuAPI project

set -e

echo "🚀 FactuAPI Setup Script"
echo "========================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker and Docker Compose first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from example..."
    cp .env.example .env
    echo "✅ .env file created. Please edit it with your configuration."
else
    echo "✅ .env file already exists."
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p logs
mkdir -p media
mkdir -p staticfiles
mkdir -p docker/nginx/ssl
echo "✅ Directories created."

# Build Docker images
echo "🐳 Building Docker images..."
docker-compose build

# Start services
echo "🚀 Starting services..."
docker-compose up -d

# Wait for database to be ready
echo "⏳ Waiting for database to be ready..."
sleep 10

# Run migrations
echo "🗄️  Running database migrations..."
docker-compose exec web python manage.py migrate

# Create superuser
echo "👤 Creating superuser..."
echo "Please provide details for the admin user:"
docker-compose exec web python manage.py createsuperuser

# Load initial data (if fixture exists)
if [ -f "fixtures/initial_data.json" ]; then
    echo "📊 Loading initial data..."
    docker-compose exec web python manage.py loaddata fixtures/initial_data.json
fi

# Collect static files
echo "📦 Collecting static files..."
docker-compose exec web python manage.py collectstatic --noinput

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "📚 Access points:"
echo "   - API Documentation: http://localhost:8000/docs/"
echo "   - Admin Interface: http://localhost:8000/admin/"
echo "   - API Root: http://localhost:8000/"
echo "   - Health Check: http://localhost:8000/health/"
echo ""
echo "🔧 Useful commands:"
echo "   - View logs: make logs"
echo "   - Access shell: make shell"
echo "   - Run tests: make test"
echo "   - Stop services: make down"
echo ""
echo "📖 For more information, check the README.md file."