from django.db import transaction
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from apps.clients.models.models import Client
from apps.individuals.models import Individual
from apps.companies.models import CompanyBranch
from apps.users.models.models import Role
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

User = get_user_model()

class UserCreationService:
    @classmethod
    @transaction.atomic
    def create_client_user(cls, creator, client, user_data):
        """
        Creates a client user with proper validation and relationships
        """
        if not client or not isinstance(client, Client):
            raise ValidationError("Invalid client provided")
        
        if not client.can_have_users:
            raise ValidationError("This client type cannot have users")

        if not user_data.get('email'):
            raise ValidationError("Email is required")
        if not user_data.get('password'):
            raise ValidationError("Password is required")

        user = User.objects.create_user(
            username=user_data.get('email'),
            email=user_data['email'],
            password=user_data['password'],
            first_name=user_data.get('first_name', ''),
            last_name=user_data.get('last_name', ''),
            client=client,
            is_staff=user_data.get('is_staff', False),
            is_verified=user_data.get('is_verified', False)
        )

        if client.is_individual_client and isinstance(client.client_object, Individual):
            user.profile_content_type = ContentType.objects.get_for_model(Individual)
            user.profile_object_id = client.client_object.id
            user.save()

        if 'role_id' in user_data:
            try:
                role = Role.objects.get(id=user_data['role_id'])
                user.roles.add(role)
            except Role.DoesNotExist:
                raise ValidationError("Specified role does not exist")

        return user

    @classmethod
    def create_system_user(cls, creator, user_data, role_id=None):
        """
        Creates a system user (admin/staff) not associated with any client
        """
        if not user_data.get('email'):
            raise ValidationError("Email is required")
        if not user_data.get('password'):
            raise ValidationError("Password is required")

        role = None
        if role_id:
            try:
                role = Role.objects.get(id=role_id)
            except Role.DoesNotExist as e:
                raise ValidationError("Specified role does not exist") from e

        user = User.objects.create_user(
            username=user_data.get('email'), 
            email=user_data['email'],
            password=user_data['password'],
            is_staff=user_data.get('is_staff', False),
            is_superuser=user_data.get('is_superuser', False),
            is_verified=user_data.get('is_verified', True), 
            first_name=user_data.get('first_name', ''),
            last_name=user_data.get('last_name', ''),
        )

        if role:
            user.roles.add(role)

        return user