"""
Custom exception handlers for FactuAPI project.
"""

import logging
from django.http import Http404
from django.core.exceptions import PermissionDenied, ValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Custom exception handler that provides consistent error responses.
    """
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if response is not None:
        custom_response_data = {
            'error': True,
            'message': 'An error occurred',
            'details': response.data,
            'status_code': response.status_code
        }

        # Customize the response based on the exception type
        if isinstance(exc, Http404):
            custom_response_data['message'] = 'Resource not found'
        elif isinstance(exc, PermissionDenied):
            custom_response_data['message'] = 'Permission denied'
        elif isinstance(exc, ValidationError):
            custom_response_data['message'] = 'Validation error'
        elif hasattr(exc, 'detail'):
            if isinstance(exc.detail, dict):
                # Handle field-specific errors
                custom_response_data['message'] = 'Validation error'
            elif isinstance(exc.detail, list):
                custom_response_data['message'] = exc.detail[0] if exc.detail else 'An error occurred'
            else:
                custom_response_data['message'] = str(exc.detail)

        # Log the error for debugging
        logger.error(
            f"API Error: {exc.__class__.__name__} - {custom_response_data['message']}",
            extra={
                'request': context.get('request'),
                'view': context.get('view'),
                'exception': exc,
            }
        )

        response.data = custom_response_data

    return response


class SRIException(Exception):
    """Custom exception for SRI-related errors."""
    pass


class InvoiceException(Exception):
    """Custom exception for invoice-related errors."""
    pass


class CertificateException(Exception):
    """Custom exception for certificate-related errors."""
    pass


class PDFGenerationException(Exception):
    """Custom exception for PDF generation errors."""
    pass