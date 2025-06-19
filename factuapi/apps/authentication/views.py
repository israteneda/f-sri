"""
Authentication views for FactuAPI.
"""
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.utils import extend_schema

from .serializers import (
    LoginSerializer, 
    UserRegistrationSerializer, 
    TokenSerializer,
    UserSerializer
)


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom token obtain pair view that returns user data with tokens.
    """
    @extend_schema(
        request=LoginSerializer,
        responses={200: TokenSerializer}
    )
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        token_data = TokenSerializer.get_token_for_user(user)
        
        return Response(token_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
@extend_schema(
    request=UserRegistrationSerializer,
    responses={201: TokenSerializer, 400: 'Bad Request'}
)
def register(request):
    """
    Register a new user and return JWT tokens.
    """
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token_data = TokenSerializer.get_token_for_user(user)
        return Response(token_data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
@extend_schema(responses={200: UserSerializer})
def profile(request):
    """
    Get current user profile.
    """
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(['PUT', 'PATCH'])
@permission_classes([permissions.IsAuthenticated])
@extend_schema(
    request=UserSerializer,
    responses={200: UserSerializer}
)
def update_profile(request):
    """
    Update current user profile.
    """
    serializer = UserSerializer(
        request.user, 
        data=request.data, 
        partial=request.method == 'PATCH'
    )
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
@extend_schema(responses={204: 'No Content'})
def logout(request):
    """
    Logout user by blacklisting the refresh token.
    """
    try:
        refresh_token = request.data.get('refresh_token')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Exception:
        return Response(
            {'error': 'Invalid token'}, 
            status=status.HTTP_400_BAD_REQUEST
        )