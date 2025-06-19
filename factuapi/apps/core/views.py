"""
Core views for FactuAPI.
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import sys


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """
    Health check endpoint for monitoring.
    """
    return Response({
        'status': 'OK',
        'environment': getattr(settings, 'ENVIRONMENT', 'development'),
        'debug': settings.DEBUG,
        'python_version': sys.version,
        'django_version': settings.DJANGO_VERSION if hasattr(settings, 'DJANGO_VERSION') else 'unknown',
    }, status=status.HTTP_200_OK)