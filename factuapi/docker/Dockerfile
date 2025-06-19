# Multi-stage Dockerfile for Django application

# Base stage
FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    gettext \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Copy requirements
COPY requirements/ /app/requirements/

# Development stage
FROM base as development

# Install development dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements/development.txt

# Copy application code
COPY . /app/

# Create non-root user for development
RUN groupadd -r django && useradd -r -g django django
RUN chown -R django:django /app
USER django

# Production stage
FROM base as production

# Install production dependencies only
RUN pip install --upgrade pip && \
    pip install -r requirements/production.txt

# Copy application code
COPY . /app/

# Collect static files
RUN python manage.py collectstatic --noinput

# Create non-root user
RUN groupadd -r django && useradd -r -g django django
RUN chown -R django:django /app
USER django

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health/ || exit 1

EXPOSE 8000