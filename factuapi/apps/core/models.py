"""
Core models for FactuAPI project.
"""

import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords


class TimeStampedModel(models.Model):
    """
    Abstract base class that provides self-updating created_at and updated_at fields.
    """
    created_at = models.DateTimeField(
        _('Created at'),
        auto_now_add=True,
        help_text=_('Date and time when the record was created')
    )
    updated_at = models.DateTimeField(
        _('Updated at'),
        auto_now=True,
        help_text=_('Date and time when the record was last updated')
    )

    class Meta:
        abstract = True


class UUIDModel(models.Model):
    """
    Abstract base class that provides a UUID primary key.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text=_('Unique identifier for this record')
    )

    class Meta:
        abstract = True


class BaseModel(TimeStampedModel, UUIDModel):
    """
    Base model that combines timestamped and UUID functionality.
    """
    history = HistoricalRecords(inherit=True)

    class Meta:
        abstract = True


class IdentificationType(TimeStampedModel):
    """
    Model for identification types (Cédula, RUC, Pasaporte, etc.)
    """
    code = models.CharField(
        _('Code'),
        max_length=2,
        unique=True,
        help_text=_('SRI identification type code')
    )
    name = models.CharField(
        _('Name'),
        max_length=100,
        help_text=_('Description of the identification type')
    )
    is_active = models.BooleanField(
        _('Is active'),
        default=True,
        help_text=_('Whether this identification type is currently active')
    )

    class Meta:
        verbose_name = _('Identification Type')
        verbose_name_plural = _('Identification Types')
        ordering = ['code']

    def __str__(self):
        return f"{self.code} - {self.name}"


class Country(TimeStampedModel):
    """
    Model for countries.
    """
    code = models.CharField(
        _('Code'),
        max_length=3,
        unique=True,
        help_text=_('ISO 3166-1 alpha-3 country code')
    )
    name = models.CharField(
        _('Name'),
        max_length=100,
        help_text=_('Country name')
    )
    is_active = models.BooleanField(
        _('Is active'),
        default=True,
        help_text=_('Whether this country is currently active')
    )

    class Meta:
        verbose_name = _('Country')
        verbose_name_plural = _('Countries')
        ordering = ['name']

    def __str__(self):
        return self.name


class Province(TimeStampedModel):
    """
    Model for provinces/states.
    """
    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name='provinces',
        verbose_name=_('Country')
    )
    code = models.CharField(
        _('Code'),
        max_length=10,
        help_text=_('Province code')
    )
    name = models.CharField(
        _('Name'),
        max_length=100,
        help_text=_('Province name')
    )
    is_active = models.BooleanField(
        _('Is active'),
        default=True,
        help_text=_('Whether this province is currently active')
    )

    class Meta:
        verbose_name = _('Province')
        verbose_name_plural = _('Provinces')
        ordering = ['country', 'name']
        unique_together = [['country', 'code']]

    def __str__(self):
        return f"{self.country.name} - {self.name}"


class City(TimeStampedModel):
    """
    Model for cities.
    """
    province = models.ForeignKey(
        Province,
        on_delete=models.CASCADE,
        related_name='cities',
        verbose_name=_('Province')
    )
    code = models.CharField(
        _('Code'),
        max_length=10,
        help_text=_('City code')
    )
    name = models.CharField(
        _('Name'),
        max_length=100,
        help_text=_('City name')
    )
    is_active = models.BooleanField(
        _('Is active'),
        default=True,
        help_text=_('Whether this city is currently active')
    )

    class Meta:
        verbose_name = _('City')
        verbose_name_plural = _('Cities')
        ordering = ['province', 'name']
        unique_together = [['province', 'code']]

    def __str__(self):
        return f"{self.province.name} - {self.name}"


class Currency(TimeStampedModel):
    """
    Model for currencies.
    """
    code = models.CharField(
        _('Code'),
        max_length=3,
        unique=True,
        help_text=_('ISO 4217 currency code')
    )
    name = models.CharField(
        _('Name'),
        max_length=100,
        help_text=_('Currency name')
    )
    symbol = models.CharField(
        _('Symbol'),
        max_length=5,
        help_text=_('Currency symbol')
    )
    is_active = models.BooleanField(
        _('Is active'),
        default=True,
        help_text=_('Whether this currency is currently active')
    )

    class Meta:
        verbose_name = _('Currency')
        verbose_name_plural = _('Currencies')
        ordering = ['code']

    def __str__(self):
        return f"{self.code} - {self.name}"


class TaxType(TimeStampedModel):
    """
    Model for tax types (IVA, ICE, etc.)
    """
    code = models.CharField(
        _('Code'),
        max_length=10,
        unique=True,
        help_text=_('Tax type code')
    )
    name = models.CharField(
        _('Name'),
        max_length=100,
        help_text=_('Tax type name')
    )
    percentage = models.DecimalField(
        _('Percentage'),
        max_digits=5,
        decimal_places=2,
        help_text=_('Tax percentage')
    )
    is_active = models.BooleanField(
        _('Is active'),
        default=True,
        help_text=_('Whether this tax type is currently active')
    )

    class Meta:
        verbose_name = _('Tax Type')
        verbose_name_plural = _('Tax Types')
        ordering = ['code']

    def __str__(self):
        return f"{self.code} - {self.name} ({self.percentage}%)"