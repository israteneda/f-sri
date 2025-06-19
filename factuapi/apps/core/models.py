"""
Core models for FactuAPI.
"""
from django.db import models
from django.utils import timezone


class TimestampedModel(models.Model):
    """
    Abstract model that provides self-updating created_at and updated_at fields.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class IdentificationType(TimestampedModel):
    """
    Types of identification for clients (Cédula, RUC, Pasaporte, etc.)
    """
    code = models.CharField(max_length=2, unique=True, help_text="SRI code for identification type")
    name = models.CharField(max_length=50, help_text="Name of identification type")
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'identification_types'
        verbose_name = 'Tipo de Identificación'
        verbose_name_plural = 'Tipos de Identificación'
        ordering = ['code']

    def __str__(self):
        return f"{self.code} - {self.name}"


class IssuingCompany(TimestampedModel):
    """
    Company that issues invoices.
    """
    identification_type = models.ForeignKey(
        IdentificationType, 
        on_delete=models.PROTECT,
        related_name='issuing_companies'
    )
    identification = models.CharField(max_length=13, unique=True)
    business_name = models.CharField(max_length=300)
    trade_name = models.CharField(max_length=300, blank=True)
    address = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    
    # SRI specific fields
    sri_environment = models.CharField(
        max_length=1, 
        choices=[('1', 'Pruebas'), ('2', 'Producción')],
        default='1'
    )
    electronic_signature = models.FileField(
        upload_to='signatures/', 
        null=True, 
        blank=True,
        help_text="P12 signature file"
    )
    signature_password = models.CharField(max_length=100, blank=True)
    
    # Configuration
    is_active = models.BooleanField(default=True)
    next_sequential = models.PositiveIntegerField(default=1)

    class Meta:
        db_table = 'issuing_companies'
        verbose_name = 'Empresa Emisora'
        verbose_name_plural = 'Empresas Emisoras'

    def __str__(self):
        return f"{self.identification} - {self.business_name}"