"""
Core views for FactuAPI project.
"""

from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """
    Health check endpoint.
    """
    return Response({
        'status': 'healthy',
        'service': 'FactuAPI',
        'version': '1.0.0'
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request):
    """
    API root endpoint with available endpoints.
    """
    return Response({
        'message': 'Welcome to FactuAPI',
        'version': '1.0.0',
        'documentation': request.build_absolute_uri('/docs/'),
        'endpoints': {
            'authentication': request.build_absolute_uri('/api/v1/auth/'),
            'companies': request.build_absolute_uri('/api/v1/companies/'),
            'clients': request.build_absolute_uri('/api/v1/clients/'),
            'products': request.build_absolute_uri('/api/v1/products/'),
            'invoices': request.build_absolute_uri('/api/v1/invoices/'),
            'reports': request.build_absolute_uri('/api/v1/reports/'),
        }
    })


# Error handlers
def bad_request(request, exception=None):
    """Custom 400 error handler."""
    return JsonResponse({
        'error': 'Bad Request',
        'message': 'The request could not be understood by the server.',
        'status_code': 400
    }, status=400)


def permission_denied(request, exception=None):
    """Custom 403 error handler."""
    return JsonResponse({
        'error': 'Permission Denied',
        'message': 'You do not have permission to access this resource.',
        'status_code': 403
    }, status=403)


def page_not_found(request, exception=None):
    """Custom 404 error handler."""
    return JsonResponse({
        'error': 'Not Found',
        'message': 'The requested resource was not found.',
        'status_code': 404
    }, status=404)


def server_error(request, exception=None):
    """Custom 500 error handler."""
    return JsonResponse({
        'error': 'Internal Server Error',
        'message': 'An internal server error occurred.',
        'status_code': 500
    }, status=500)