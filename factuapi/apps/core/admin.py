"""
Admin configuration for core models.
"""
from django.contrib import admin
from .models import IdentificationType, IssuingCompany


@admin.register(IdentificationType)
class IdentificationTypeAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['code', 'name']
    ordering = ['code']


@admin.register(IssuingCompany)
class IssuingCompanyAdmin(admin.ModelAdmin):
    list_display = ['identification', 'business_name', 'trade_name', 'is_active', 'created_at']
    list_filter = ['identification_type', 'sri_environment', 'is_active', 'created_at']
    search_fields = ['identification', 'business_name', 'trade_name', 'email']
    ordering = ['business_name']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('identification_type', 'identification', 'business_name', 'trade_name')
        }),
        ('Contacto', {
            'fields': ('address', 'email', 'phone')
        }),
        ('Configuración SRI', {
            'fields': ('sri_environment', 'electronic_signature', 'signature_password')
        }),
        ('Configuración', {
            'fields': ('is_active', 'next_sequential')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )