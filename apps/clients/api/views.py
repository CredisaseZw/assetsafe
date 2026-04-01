from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.core.exceptions import ValidationError
from django.db.models import Q
from apps.clients.models.models import Client
from apps.individuals.models import Individual
from apps.companies.models import CompanyBranch
from apps.clients.api.serializers import ClientCreateUpdateSerializer, FullClientSerializer, MinimalClientSerializer
from apps.common.services.tasks import send_notification
from apps.users.services.user_service import UserCreationService
from apps.users.api.serializers import UserSerializer, MinimalUserSerializer
from django.contrib.auth import get_user_model
from django.conf import settings
from django.shortcuts import get_object_or_404
import logging
logger = logging.getLogger(__name__)

User = get_user_model()

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = FullClientSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ClientCreateUpdateSerializer
        elif self.action in ['search']:
            return MinimalClientSerializer
        return FullClientSerializer

    @action(detail=True, methods=['post'], url_path='create-user')
    def create_user(self, request, pk=None):
        """
        Create a user for this client with specified role
        """
        try:
            client = Client.objects.select_related(
                'client_content_type'
            ).get(pk=pk)
            
            linked_object = client.client_object
            
            if not linked_object:
                return Response(
                    {"detail": "No linked entity found for this client"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
        except Client.DoesNotExist:
            return Response(
                {"detail": f"Client with ID {pk} does not exist"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if not client.can_have_users:
            return Response(
                {"detail": "This client type cannot have users associated with it"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user_data = request.data.copy()
        user_data['client_id'] = client.id
        
        if client.is_individual_client:
            if not isinstance(linked_object, Individual):
                return Response(
                    {"detail": "Client is marked as individual but linked object is not an Individual"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # if linked_object.email and user_data.get('email', '').lower() != linked_object.email.lower():
            #     return Response(
            #         {"detail": "Email must match the individual's registered email"},
            #         status=status.HTTP_400_BAD_REQUEST
            #     )
            
            if not user_data.get('email'):
                user_data['email'] = linked_object.email

        try:
            with transaction.atomic():
                user = UserCreationService.create_client_user(
                    creator=request.user,
                    client=client,
                    user_data=user_data
                )
                if user:
                    print(f"User {user.email} created for client {client.name}")
                    self._send_welcome_email(user, user_data.get('password'))

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
            logger.error(f"Error creating user for client {pk}: {str(e)}", exc_info=True)
            return Response(
                {"detail": "An error occurred while creating user"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    @action(detail=False, methods=['get'], url_path='users')
    def list_users(self, request):
        """
        List all users associated with a given client ID passed as a query param (?pk=1)
        """
        client_pk = request.query_params.get('client_id')
        if not client_pk:
            return Response({'error': 'Missing client pk in query params'}, status=status.HTTP_400_BAD_REQUEST)

        client = get_object_or_404(Client, pk=client_pk)
        users = User.objects.filter(client=client).distinct()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    @action(detail=False, methods=['get'], url_path='search')
    def search(self, request):
        """
        Search for clients by name or external client ID
        """
        query = request.query_params.get('q', '').strip()
        if not query:
            return Response(
                {"detail": "Query parameter 'q' is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        clients = Client.objects.filter(
            Q(name__icontains=query) | Q(external_client_id__icontains=query)
        ).distinct()
        
        serializer = MinimalClientSerializer(clients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def _send_welcome_email(self, user, plaintext_password):
        """Send welcome email with login credentials"""
        context = {
            'user': user,
            'password': plaintext_password,
            'login_url': settings.FRONTEND_LOGIN_URL,
            'platform_name': settings.PLATFORM_NAME
        }
        
        recipient_id = user.client.client_object_id
        if user.client.is_individual_client:
            recipient_type = 'individual'
        else:
            recipient_type = 'company'
        
        send_notification(
            recipient_type=recipient_type,
            recipient_id=recipient_id,
            notification_type='NEW_CLIENT_USER',
            context=context,
            sender_id=self.request.user.id if self.request.user.is_authenticated else None,
            template_name='welcome_client_user',
            subject=f"Welcome to {settings.PLATFORM_NAME}"
        )