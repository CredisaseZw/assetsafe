import logging
from django.db import transaction
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from apps.clients.models.models import Client
from apps.individuals.models import Individual
from apps.companies.models import CompanyBranch
from apps.users.models.models import Role
from django.conf import settings
from apps.common.services.tasks import send_notification

logger = logging.getLogger(__name__)

User = get_user_model()


def _log_user_creation(user, creator, logger_instance=None):
    """Emit an audit log entry for user creation (DB + file)."""
    try:
        from apps.users.services.audit_service import create_audit_log

        create_audit_log(
            request=None,
            action="user.create",
            resource_type="CustomUser",
            resource_id=user.pk,
            details={
                "username": user.username,
                "email": user.email,
                "created_by": creator.username if creator else "system",
                "is_staff": user.is_staff,
            },
            logger=logger_instance or logger,
        )
    except Exception:
        # Never let audit logging break the main flow
        logger.exception("Failed to write audit log for user.create (user_id=%s)", user.pk)


def _log_role_assignment(user, role, creator, logger_instance=None):
    """Emit an audit log entry for role assignment (DB + file)."""
    try:
        from apps.users.services.audit_service import create_audit_log

        create_audit_log(
            request=None,
            action="user.role_assigned",
            resource_type="CustomUser",
            resource_id=user.pk,
            details={
                "username": user.username,
                "role": role.name,
                "assigned_by": creator.username if creator else "system",
            },
            logger=logger_instance or logger,
        )
    except Exception:
        logger.exception(
            "Failed to write audit log for user.role_assigned (user_id=%s, role=%s)",
            user.pk,
            role.name,
        )


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

        if not user_data.get("email"):
            raise ValidationError("Email is required")
        if not user_data.get("password"):
            raise ValidationError("Password is required")

        user = User.objects.create_user(
            username=user_data.get("email"),
            email=user_data["email"],
            password=user_data["password"],
            first_name=user_data.get("first_name", ""),
            last_name=user_data.get("last_name", ""),
            client=client,
            is_staff=user_data.get("is_staff", False),
            is_verified=user_data.get("is_verified", False),
        )

        if client.is_individual_client and isinstance(client.client_object, Individual):
            user.profile_content_type = ContentType.objects.get_for_model(Individual)
            user.profile_object_id = client.client_object.id
            user.save()

        if "role_id" in user_data:
            try:
                role = Role.objects.get(id=user_data["role_id"])
                user.roles.add(role)
                _log_role_assignment(user, role, creator)
            except Role.DoesNotExist:
                raise ValidationError("Specified role does not exist")

        _log_user_creation(user, creator)

        # Send welcome notification to client user
        send_notification(
            recipient_type="user",
            recipient_id=user.id,
            notification_type="WELCOME_CLIENT",
            context={
                "user": user,
                "client": client,
            },
            template_name="welcome_client",
            subject="Welcome to AssetSafe!",
        )

        return user

    @classmethod
    def create_system_user(cls, creator, user_data, role_id=None):
        """
        Creates a system user (admin/staff) not associated with any client
        """
        if not user_data.get("email"):
            raise ValidationError("Email is required")
        if not user_data.get("password"):
            raise ValidationError("Password is required")

        role = None
        if role_id:
            try:
                role = Role.objects.get(id=role_id)
            except Role.DoesNotExist as e:
                raise ValidationError("Specified role does not exist") from e

        user = User.objects.create_user(
            username=user_data.get("email"),
            email=user_data["email"],
            password=user_data["password"],
            is_staff=user_data.get("is_staff", False),
            is_superuser=user_data.get("is_superuser", False),
            is_verified=user_data.get("is_verified", True),
            first_name=user_data.get("first_name", ""),
            last_name=user_data.get("last_name", ""),
        )

        if role:
            user.roles.add(role)
            _log_role_assignment(user, role, creator)

        _log_user_creation(user, creator)

        # Send welcome notification to system user
        send_notification(
            recipient_type="user",
            recipient_id=user.id,
            notification_type="WELCOME_USER",
            context={
                "user": user,
            },
            template_name="welcome_user",
            subject="Welcome to AssetSafe!",
        )

        return user
