"""User-related API views, including authentication, user management, and role management."""

import json
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, viewsets
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.db import transaction
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.exceptions import ValidationError
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from apps.common.services.tasks import send_notification
from django.contrib.sites.shortcuts import get_current_site
from drf_spectacular.utils import extend_schema, OpenApiResponse, inline_serializer
from rest_framework import serializers as drf_serializers

from apps.users.api.authentication import CookieJWTAuthentication
from apps.users.api.serializers import (
    CustomTokenObtainPairSerializer,
    UserSerializer,
    UserCreateSerializer,
    RoleSerializer,
    RoleMinimalSerializer,
    PasswordChangeSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
)
from apps.users.models import Role
from apps.users.services.user_service import UserCreationService
from apps.users.utils.cookies import (
    delete_jwt_cookies,
    create_response_with_cookies,
)
from apps.users.utils.tokens import password_reset_token_generator

logger = logging.getLogger(__name__)
User = get_user_model()
from django.utils import timezone


class LoginView(APIView):
    """
    Custom login view that handles cookie setting properly.
    """

    permission_classes = []  # Allow anyone to access login

    @extend_schema(
        summary="Obtain JWT tokens",
        description=(
            "Authenticate with email and password. On success the response sets "
            "`access_token` and `refresh_token` HTTP-only cookies and returns basic "
            "user information. All subsequent API requests are authenticated via the "
            "`access_token` cookie."
        ),
        request=inline_serializer(
            name="LoginRequest",
            fields={
                "email": drf_serializers.EmailField(),
                "password": drf_serializers.CharField(),
            },
        ),
        responses={
            200: inline_serializer(
                name="LoginResponse",
                fields={
                    "user": inline_serializer(
                        name="LoginUserInfo",
                        fields={
                            "id": drf_serializers.IntegerField(),
                            "username": drf_serializers.CharField(),
                            "email": drf_serializers.EmailField(),
                            "user_type": drf_serializers.CharField(),
                            "is_verified": drf_serializers.BooleanField(),
                            "client": drf_serializers.IntegerField(allow_null=True),
                        },
                    ),
                    "message": drf_serializers.CharField(),
                },
            ),
            401: OpenApiResponse(description="Invalid credentials"),
            403: OpenApiResponse(description="Account not verified"),
        },
        auth=[],
    )
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

    @extend_schema(
        summary="Invalidate session and clear JWT cookies",
        description="Clears the `access_token` and `refresh_token` cookies set during login.",
        request=None,
        responses={
            200: inline_serializer(
                name="LogoutResponse",
                fields={"message": drf_serializers.CharField()},
            ),
            500: OpenApiResponse(description="Unexpected server error"),
        },
        auth=[],
    )
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

    @extend_schema(
        summary="Refresh the JWT access token",
        description=(
            "Uses the `refresh_token` cookie to issue a new `access_token` cookie. "
            "The request must carry a valid refresh token in the cookie."
        ),
        request=None,
        responses={
            200: inline_serializer(
                name="RefreshTokenResponse",
                fields={"message": drf_serializers.CharField()},
            ),
            401: OpenApiResponse(description="Refresh token missing or invalid"),
        },
    )
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

    @extend_schema(
        summary="Retrieve the currently authenticated user",
        description="Returns the full profile of the user identified by the current JWT access token.",
        responses={200: "UserSerializer"},
    )
    @method_decorator(cache_page(60 * 2))
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class CheckCSRFView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Verify CSRF token validity",
        description="Simple endpoint to confirm the CSRF token included in the request is valid.",
        request=None,
        responses={
            200: inline_serializer(
                name="CSRFCheckResponse",
                fields={"message": drf_serializers.CharField()},
            )
        },
    )
    def get(self, request):
        return Response({"message": "CSRF token is valid"}, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return UserCreateSerializer
        return UserSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
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
                client = user_data.get("client_id")
                role_id = user_data.get("role_id")

                if client:
                    # Create client user
                    user = UserCreationService.create_client_user(
                        creator=request.user, client=client, user_data=user_data
                    )
                else:
                    # Create system user
                    user = UserCreationService.create_system_user(
                        creator=request.user, user_data=user_data, role_id=role_id
                    )

                return Response(
                    UserSerializer(user).data, status=status.HTTP_201_CREATED
                )

        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"detail": "An error occurred while creating user"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def perform_update(self, serializer):
        old_email = serializer.instance.email
        user = serializer.save()

        # Check if email was changed
        if old_email and user.email and old_email.lower() != user.email.lower():
            # Send notification to the new email
            send_notification(
                recipient_type="user",
                recipient_id=user.id,
                notification_type="EMAIL_CHANGED",
                context={
                    "user": user,
                    "old_email": old_email,
                },
                template_name="email_changed",
                subject="Your Email Address Has Been Changed",
            )


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

    @extend_schema(
        summary="List roles (minimal)",
        description="Returns a lightweight list of all roles with only id, name and description fields.",
        responses={200: "RoleMinimalSerializer(many=True)"},
    )
    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def minimal(self, request):
        """
        Get a minimal list of roles with only id, name, and description
        """
        roles = Role.objects.all()
        serializer = RoleMinimalSerializer(roles, many=True)
        return Response(serializer.data)


class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Change the authenticated user's password",
        request="PasswordChangeSerializer",
        responses={
            200: inline_serializer(
                name="PasswordChangeResponse",
                fields={"message": drf_serializers.CharField()},
            ),
            400: OpenApiResponse(description="Validation error (current password wrong or new passwords mismatch)"),
        },
    )
    def post(self, request):
        serializer = PasswordChangeSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            request.user.set_password(serializer.validated_data["new_password"])
            request.user.last_password_change = timezone.now()
            request.user.save()

            # Send notification using the template
            send_notification(
                recipient_type="user",
                recipient_id=request.user.id,
                notification_type="PASSWORD_CHANGED",
                context={
                    "user": request.user,
                },
                template_name="password_changed",
                subject="Your Password Has Been Changed",
            )

            return Response(
                {"message": "Password changed successfully"}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetRequestView(APIView):
    permission_classes = []

    @extend_schema(
        summary="Request a password reset email",
        description=(
            "Sends a password-reset link to the supplied email address if an account "
            "exists. Always returns HTTP 200 to avoid email enumeration."
        ),
        request="PasswordResetRequestSerializer",
        responses={
            200: inline_serializer(
                name="PasswordResetRequestResponse",
                fields={"message": drf_serializers.CharField()},
            ),
            400: OpenApiResponse(description="Validation error"),
        },
        auth=[],
    )
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            try:
                user = User.objects.get(email=email)
                token = password_reset_token_generator.make_token(user)
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                current_site = get_current_site(request)

                send_notification(
                    recipient_type="user",
                    recipient_id=user.id,
                    notification_type="PASSWORD_RESET",
                    context={
                        "token": token,
                        "uidb64": uidb64,
                        "user": user,
                        "protocol": "https" if request.is_secure() else "http",
                        "domain": current_site.domain,
                    },
                    template_name="password_reset",
                    subject="Password Reset Request",
                )

                return Response(
                    {"message": "Password reset link sent to your email"},
                    status=status.HTTP_200_OK,
                )
            except User.DoesNotExist:
                return Response(
                    {
                        "message": "If an account with that email exists, a password reset link has been sent."
                    },
                    status=status.HTTP_200_OK,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmView(APIView):
    permission_classes = []

    @extend_schema(
        summary="Confirm a password reset and set a new password",
        description=(
            "Validates the `uidb64` / `token` pair from the reset email and updates "
            "the user's password to the supplied value."
        ),
        request="PasswordResetConfirmSerializer",
        responses={
            200: inline_serializer(
                name="PasswordResetConfirmResponse",
                fields={"message": drf_serializers.CharField()},
            ),
            400: OpenApiResponse(description="Invalid or expired token, or passwords do not match"),
        },
        auth=[],
    )
    def post(self, request, uidb64, token):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            try:
                uid = force_str(urlsafe_base64_decode(uidb64))
                user = User.objects.get(pk=uid)
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                user = None

            if user is not None and password_reset_token_generator.check_token(
                user, token
            ):
                user.set_password(serializer.validated_data["new_password"])
                user.last_password_change = timezone.now()
                user.save()

                # Send notification using the template
                send_notification(
                    recipient_type="user",
                    recipient_id=user.id,
                    notification_type="PASSWORD_CHANGED",
                    context={
                        "user": user,
                    },
                    template_name="password_changed",
                    subject="Your Password Has Been Reset",
                )

                return Response(
                    {"message": "Password has been reset successfully"},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": "Invalid or expired token"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
