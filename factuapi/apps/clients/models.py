"""
Client models for FactuAPI.
"""
from django.db import models
from apps.core.models import TimestampedModel, IdentificationType


class Client(TimestampedModel):
    """
    Client/Customer model for invoicing.
    """
    identification_type = models.ForeignKey(
        IdentificationType,
        on_delete=models.PROTECT,
        related_name='clients'
    )
    identification = models.CharField(max_length=13, help_text="Identification number")
    business_name = models.CharField(max_length=300, help_text="Business or person name")
    trade_name = models.CharField(max_length=300, blank=True, help_text="Commercial name")
    address = models.TextField(help_text="Full address")
    email = models.EmailField(blank=True, help_text="Email address")
    phone = models.CharField(max_length=20, blank=True, help_text="Phone number")
    
    # Additional fields
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True, help_text="Additional notes")

    class Meta:
        db_table = 'clients'
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        unique_together = ['identification_type', 'identification']
        ordering = ['business_name']

    def __str__(self):
        return f"{self.identification} - {self.business_name}"

    @property
    def full_name(self):
        """Return business name or trade name if available."""
        return self.trade_name if self.trade_name else self.business_name