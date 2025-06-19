"""
Test cases for core app.
"""
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from .models import IdentificationType, IssuingCompany


class HealthCheckTestCase(APITestCase):
    """Test cases for health check endpoint."""

    def test_health_check_endpoint(self):
        """Test that health check endpoint returns OK."""
        url = reverse('core:health_check')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'OK')
        self.assertIn('environment', response.data)
        self.assertIn('debug', response.data)


class IdentificationTypeModelTestCase(TestCase):
    """Test cases for IdentificationType model."""

    def setUp(self):
        self.identification_type = IdentificationType.objects.create(
            code='05',
            name='Cédula'
        )

    def test_string_representation(self):
        """Test string representation of IdentificationType."""
        expected = f"{self.identification_type.code} - {self.identification_type.name}"
        self.assertEqual(str(self.identification_type), expected)

    def test_creation(self):
        """Test IdentificationType creation."""
        self.assertTrue(isinstance(self.identification_type, IdentificationType))
        self.assertEqual(self.identification_type.code, '05')
        self.assertEqual(self.identification_type.name, 'Cédula')
        self.assertTrue(self.identification_type.is_active)


class IssuingCompanyModelTestCase(TestCase):
    """Test cases for IssuingCompany model."""

    def setUp(self):
        self.identification_type = IdentificationType.objects.create(
            code='04',
            name='RUC'
        )
        self.issuing_company = IssuingCompany.objects.create(
            identification_type=self.identification_type,
            identification='1234567890001',
            business_name='Test Company SA',
            address='Test Address 123',
            email='test@company.com'
        )

    def test_string_representation(self):
        """Test string representation of IssuingCompany."""
        expected = f"{self.issuing_company.identification} - {self.issuing_company.business_name}"
        self.assertEqual(str(self.issuing_company), expected)

    def test_creation(self):
        """Test IssuingCompany creation."""
        self.assertTrue(isinstance(self.issuing_company, IssuingCompany))
        self.assertEqual(self.issuing_company.identification, '1234567890001')
        self.assertEqual(self.issuing_company.business_name, 'Test Company SA')
        self.assertTrue(self.issuing_company.is_active)
        self.assertEqual(self.issuing_company.next_sequential, 1)