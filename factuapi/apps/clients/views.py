"""
Client views for FactuAPI.
"""
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema

from .models import Client
from .serializers import ClientSerializer, ClientCreateSerializer


class ClientViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing clients.
    """
    queryset = Client.objects.select_related('identification_type').all()
    serializer_class = ClientSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['identification_type', 'is_active']
    search_fields = ['identification', 'business_name', 'trade_name', 'email']
    ordering_fields = ['business_name', 'created_at']
    ordering = ['business_name']

    def get_serializer_class(self):
        if self.action == 'create':
            return ClientCreateSerializer
        return ClientSerializer

    @extend_schema(
        description="Search clients by identification number",
        responses={200: ClientSerializer}
    )
    @action(detail=False, methods=['get'])
    def search_by_identification(self, request):
        """Search client by identification number."""
        identification = request.query_params.get('identification')
        if not identification:
            return Response(
                {'error': 'identification parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            client = Client.objects.select_related('identification_type').get(
                identification=identification
            )
            serializer = self.get_serializer(client)
            return Response(serializer.data)
        except Client.DoesNotExist:
            return Response(
                {'error': 'Client not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )

    @extend_schema(
        description="Get client statistics",
        responses={200: 'Client statistics'}
    )
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get client statistics."""
        total_clients = Client.objects.count()
        active_clients = Client.objects.filter(is_active=True).count()
        
        return Response({
            'total_clients': total_clients,
            'active_clients': active_clients,
            'inactive_clients': total_clients - active_clients,
        })