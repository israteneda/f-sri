"""
Core admin configuration for FactuAPI project.
"""

from django.contrib import admin
from .models import (
    IdentificationType,
    Country,
    Province,
    City,
    Currency,
    TaxType,
)


@admin.register(IdentificationType)
class IdentificationTypeAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('code', 'name')
    ordering = ('code',)


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('code', 'name')
    ordering = ('name',)


@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'country', 'is_active', 'created_at')
    list_filter = ('country', 'is_active', 'created_at')
    search_fields = ('code', 'name', 'country__name')
    ordering = ('country', 'name')


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'province', 'is_active', 'created_at')
    list_filter = ('province__country', 'province', 'is_active', 'created_at')
    search_fields = ('code', 'name', 'province__name')
    ordering = ('province', 'name')


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'symbol', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('code', 'name')
    ordering = ('code',)


@admin.register(TaxType)
class TaxTypeAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'percentage', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('code', 'name')
    ordering = ('code',)