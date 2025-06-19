"""
Client serializers for FactuAPI.
"""
from rest_framework import serializers
from .models import Client
from apps.core.models import IdentificationType


class IdentificationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = IdentificationType
        fields = ['id', 'code', 'name']


class ClientSerializer(serializers.ModelSerializer):
    identification_type_detail = IdentificationTypeSerializer(source='identification_type', read_only=True)
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = Client
        fields = [
            'id', 'identification_type', 'identification_type_detail',
            'identification', 'business_name', 'trade_name', 'full_name',
            'address', 'email', 'phone', 'is_active', 'notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_identification(self, value):
        """Validate identification number format."""
        # Add Ecuador-specific validation here
        if not value.isdigit():
            raise serializers.ValidationError("Identification must contain only numbers.")
        return value


class ClientCreateSerializer(ClientSerializer):
    """Serializer for creating clients with minimal required fields."""
    
    class Meta(ClientSerializer.Meta):
        fields = [
            'identification_type', 'identification', 'business_name',
            'address', 'email', 'phone'
        ]