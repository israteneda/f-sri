"""
Test cases for clients app.
"""
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from apps.core.models import IdentificationType
from .models import Client


class ClientModelTestCase(TestCase):
    """Test cases for Client model."""

    def setUp(self):
        self.identification_type = IdentificationType.objects.create(
            code='05',
            name='Cédula'
        )
        self.client_instance = Client.objects.create(
            identification_type=self.identification_type,
            identification='1234567890',
            business_name='John Doe',
            address='Test Address 123',
            email='john@example.com'
        )

    def test_string_representation(self):
        """Test string representation of Client."""
        expected = f"{self.client_instance.identification} - {self.client_instance.business_name}"
        self.assertEqual(str(self.client_instance), expected)

    def test_full_name_property(self):
        """Test full_name property returns business_name when no trade_name."""
        self.assertEqual(self.client_instance.full_name, self.client_instance.business_name)
        
        # Test with trade_name
        self.client_instance.trade_name = 'John\'s Store'
        self.assertEqual(self.client_instance.full_name, 'John\'s Store')


class ClientAPITestCase(APITestCase):
    """Test cases for Client API endpoints."""

    def setUp(self):
        # Create user and authenticate
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        
        # Create test data
        self.identification_type = IdentificationType.objects.create(
            code='05',
            name='Cédula'
        )
        self.client_data = {
            'identification_type': self.identification_type.id,
            'identification': '1234567890',
            'business_name': 'Test Client',
            'address': 'Test Address 123',
            'email': 'client@example.com'
        }

    def test_create_client(self):
        """Test creating a client via API."""
        url = '/api/v1/clients/'
        response = self.client.post(url, self.client_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Client.objects.count(), 1)
        self.assertEqual(Client.objects.get().business_name, 'Test Client')

    def test_list_clients(self):
        """Test listing clients via API."""
        Client.objects.create(**self.client_data)
        
        url = '/api/v1/clients/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_search_client_by_identification(self):
        """Test searching client by identification."""
        Client.objects.create(**self.client_data)
        
        url = '/api/v1/clients/search_by_identification/'
        response = self.client.get(url, {'identification': '1234567890'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['identification'], '1234567890')

    def test_client_stats(self):
        """Test client statistics endpoint."""
        Client.objects.create(**self.client_data)
        
        url = '/api/v1/clients/stats/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_clients'], 1)
        self.assertEqual(response.data['active_clients'], 1)