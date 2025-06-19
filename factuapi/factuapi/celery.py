"""
Celery configuration for FactuAPI project.
"""

import os
from celery import Celery
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'factuapi.settings.development')

app = Celery('factuapi')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# Celery beat schedule for periodic tasks
app.conf.beat_schedule = {
    'cleanup-expired-tokens': {
        'task': 'apps.authentication.tasks.cleanup_expired_tokens',
        'schedule': 3600.0,  # Run every hour
    },
    'send-pending-notifications': {
        'task': 'apps.notifications.tasks.send_pending_notifications',
        'schedule': 300.0,  # Run every 5 minutes
    },
    'generate-daily-reports': {
        'task': 'apps.reports.tasks.generate_daily_reports',
        'schedule': 86400.0,  # Run daily
    },
    'check-sri-authorization-status': {
        'task': 'apps.invoices.tasks.check_sri_authorization_status',
        'schedule': 600.0,  # Run every 10 minutes
    },
}

app.conf.timezone = 'America/Guayaquil'

@app.task(bind=True)
def debug_task(self):
    """Debug task for testing Celery functionality."""
    print(f'Request: {self.request!r}')