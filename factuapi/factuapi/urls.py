"""
URL configuration for FactuAPI project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

# API versioning
api_v1_patterns = [
    path('auth/', include('apps.authentication.urls')),
    path('companies/', include('apps.companies.urls')),
    path('clients/', include('apps.clients.urls')),
    path('products/', include('apps.products.urls')),
    path('invoices/', include('apps.invoices.urls')),
    path('reports/', include('apps.reports.urls')),
    path('notifications/', include('apps.notifications.urls')),
]

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Health checks
    path('health/', include('health_check.urls')),
    
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # API endpoints
    path('api/v1/', include(api_v1_patterns)),
    
    # Core endpoints
    path('', include('apps.core.urls')),
]

# Development-specific URLs
if settings.DEBUG:
    import debug_toolbar
    
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
    
    # Serve media files in development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Django Silk profiling (development only)
if settings.DEBUG and 'silk' in settings.INSTALLED_APPS:
    urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]

# Prometheus metrics
if 'django_prometheus' in settings.INSTALLED_APPS:
    urlpatterns += [path('', include('django_prometheus.urls'))]

# Custom error handlers
handler400 = 'apps.core.views.bad_request'
handler403 = 'apps.core.views.permission_denied'
handler404 = 'apps.core.views.page_not_found'
handler500 = 'apps.core.views.server_error'