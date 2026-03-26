from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, viewsets
from apps.users.api.authentication import CookieJWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.db import transaction
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.exceptions import ValidationError
from apps.users.api.serializers import CustomTokenObtainPairSerializer, UserSerializer, UserCreateSerializer, RoleSerializer, RoleMinimalSerializer
from apps.users.models import Role
from apps.users.services.user_service import UserCreationService
from apps.users.utils.cookies import (
    delete_jwt_cookies,
    create_response_with_cookies,
)
import json
import logging
logger = logging.getLogger(__name__)
User = get_user_model()

class LoginView(APIView):
    """
    Custom login view that handles cookie setting properly.
    """

    permission_classes = []  # Allow anyone to access login

    def post(self, request, *args, **kwargs):
        try:
            # Use the serializer to validate credentials
            serializer = CustomTokenObtainPairSerializer(
                data=request.data, context={"request": request}
            )
            serializer.is_valid(raise_exception=True)

            # Get the validated data
            data = serializer.validated_data

            # Create response with cookies
            response_data = {"user": data["user"], "message": "Login successful"}

            response = create_response_with_cookies(
                data=response_data,
                status_code=status.HTTP_200_OK,
                access_token=data["access"],
                refresh_token=data["refresh"],
            )

            return response

        except Exception as e:
            print(f"Login error: {e}")
            logger.error(f"Login error: {str(e)}")

            # Handle specific error cases
            error_message = str(e)
            if "not verified" in error_message.lower():
                return Response(
                    {"error": "Account not verified. Please verify your account."},
                    status=status.HTTP_403_FORBIDDEN,
                )
            elif "credentials" in error_message.lower():
                return Response(
                    {"error": "Invalid credentials"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
            else:
                return Response(
                    {"error": "Authentication failed"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )


class LogoutView(APIView):
    permission_classes = []  # Allow logout without authentication

    def post(self, request):
        try:
            # Create simple response
            response_data = {"message": "Logout successful"}
            response = HttpResponse(
                json.dumps(response_data),
                status=status.HTTP_200_OK,
                content_type="application/json",
            )

            # Delete cookies
            response = delete_jwt_cookies(response)

            return response

        except Exception as e:
            logger.error(f"Logout error: {str(e)}")
            return Response(
                {"error": "Logout failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class RefreshTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            from apps.users.utils.cookies import get_tokens_from_request

            tokens = get_tokens_from_request(request)
            refresh_token = tokens["refresh_token"]

            if not refresh_token:
                return Response(
                    {"error": "Refresh token not found"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            # Create new access token from refresh token
            token = RefreshToken(refresh_token)
            new_access_token = str(token.access_token)

            # Create response with new access token cookie
            response_data = {"message": "Token refreshed successfully"}
            response = create_response_with_cookies(
                data=response_data,
                status_code=status.HTTP_200_OK,
                access_token=new_access_token,
            )

            return response

        except Exception as e:
            logger.error(f"Token refresh error: {str(e)}")
            return Response(
                {"error": "Invalid refresh token"}, status=status.HTTP_401_UNAUTHORIZED
            )

class CurrentUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @method_decorator(cache_page(60*2))  
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class CheckCSRFView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "CSRF token is valid"}, status=status.HTTP_200_OK)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return UserCreateSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return super().get_permissions()

    def create(self, request):
        """
        Create either a system user or client user based on provided data
        """
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            with transaction.atomic():
                user_data = serializer.validated_data
                client = user_data.get('client_id')
                role_id = user_data.get('role_id')
                
                if client:
                    # Create client user
                    user = UserCreationService.create_client_user(
                        creator=request.user,
                        client=client,
                        user_data=user_data
                    )
                else:
                    # Create system user
                    user = UserCreationService.create_system_user(
                        creator=request.user,
                        user_data=user_data,
                        role_id=role_id
                    )
                
                return Response(
                    UserSerializer(user).data,
                    status=status.HTTP_201_CREATED
                )
                
        except ValidationError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"detail": "An error occurred while creating user"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def minimal(self, request):
        """
        Get a minimal list of roles with only id, name, and description
        """
        roles = Role.objects.all()
        serializer = RoleMinimalSerializer(roles, many=True)
        return Response(serializer.data)