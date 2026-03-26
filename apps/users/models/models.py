# users/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser, Permission
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import transaction
from apps.users.utils.manager import CustomUserManager, generate_unique_username
from apps.individuals.models.models import Individual
from apps.companies.models.models import Company
from apps.common.models.base_models import BaseModel
from apps.clients.models.models import Client

class CustomUser(AbstractUser):

    email = models.EmailField(_('email address'), unique=True, blank=True, null=True,
            help_text=_("Required. Unique email address for the user."))
    
    is_verified = models.BooleanField(default=False,
                help_text=_("Designates whether the user's account has been verified (e.g., email/phone)."))
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True,
                                        help_text=_("Profile picture of the user."))
    last_password_change = models.DateTimeField(null=True, blank=True,
                                                help_text=_("Timestamp of the user's last password change."))
    profile_content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL,null=True,blank=True,related_name='user_profiles',
                help_text=_("The content type of the associated Individual or Company profile."),
                )

    profile_object_id = models.PositiveIntegerField(null=True, blank=True,
                                            help_text=_("The ID of the associated Individual or Company profile."))
    profile_object = GenericForeignKey('profile_content_type', 'profile_object_id')

    can_send_email = models.BooleanField(default=True,
                    help_text=_("Designates whether the user is allowed to send emails from the system."))

    roles = models.ManyToManyField('Role', blank=True, related_name='users',
                    help_text=_("The specific roles assigned to this user, granting specific permissions."))
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True, related_name='users',
                                help_text=_("The client (Individual or Company) this user belongs to.")
                            )
    last_login = models.DateTimeField(_('last login'), null=True, blank=True,default=timezone.now,
                help_text=_("The date and time of the user's last login."))

    objects = CustomUserManager()

    REQUIRED_FIELDS = ['email']

    class Meta(AbstractUser.Meta):
        app_label = 'users'
        swappable = 'AUTH_USER_MODEL'
        verbose_name = _("Custom User")
        verbose_name_plural = _("Custom Users")
        ordering = []
        
    
    def __str__(self):
        full_name = self.get_full_name()
        if full_name:
            return f"{full_name} ({self.username})"
        return self.username or self.email or f"User {self.pk}"

    
    def get_associated_client(self):
        """Returns the client this user directly belongs to."""
        return self.client.name if self.client else "Clientless User"
    
    def clean(self):
        super().clean()
        if not self.is_staff and not self.client:
            raise ValidationError(
                _("Non-staff users must be assigned to a client.")
            )

    def get_associated_individual(self):
        if self.profile_object and isinstance(self.profile_object, Individual):
            return self.profile_object
        return None

    def has_perm(self, perm, obj=None):
        """
        Returns True if the user has the specified permission, checking both
        direct permissions and permissions granted via roles.
        """
        if super().has_perm(perm, obj=obj):
            return True

        if not self.is_active or self.is_anonymous:
            return False

        return any(role.has_perm(perm) for role in self.roles.all())

    def get_all_permissions(self, obj=None):
        """
        Returns a set of permission strings that this user has, through their
        direct permissions, groups, and assigned roles.
        """
        permissions = set(super().get_all_permissions(obj=obj))
        for role in self.roles.all():
            permissions.update(role.get_all_permissions())
        return permissions

    def get_associated_company(self):
        """Returns the Company object associated with this user's client, if applicable."""
        if self.client and self.client.is_company_client:
            return self.client.get_linked_entity
        return None
    @property
    def user_type(self):
        """
        Returns the type of user based on their client association.
        'Individual' if associated with an Individual, 'Company' if associated with a Company.
        """
        if self.is_staff or self.is_superuser:
            return 'Staff'
        if self.client and self.client.is_individual_client:
            return 'Individual'
        if self.client and self.client.is_company_client:
            return 'Company'
        return self.client.client_type if self.client else 'Unknown'


    def save(self, *args, **kwargs):
        self.full_clean() 
    
        if not self.username:
            self.username = generate_unique_username(self.email or f"user_{self.pk}")
        super().save(*args, **kwargs)
        


class Role(models.Model):
    name = models.CharField(max_length=100, unique=True,
                            help_text=_("Unique name for the role (e.g., 'Property Manager', 'Tenant User')."))
    description = models.TextField(blank=True,
                help_text=_("Detailed description of what this role entails."))
    permissions = models.ManyToManyField(Permission, blank=True, related_name='roles',
                help_text=_("Specific permissions granted to users with this role."))
    is_active = models.BooleanField(default=True,
                                    help_text=_("Designates whether this role is currently active and assignable."))

    class Meta:
        verbose_name = _('role')
        verbose_name_plural = _('roles')
        ordering = ['name']

    def __str__(self):
        return self.name

    def has_perm(self, perm_codename):
        """
        Checks if this role grants a specific permission.
        'perm_codename' should be in the format 'app_label.permission_codename'.
        """
        if not self.is_active:
            return False

        try:
            app_label, codename = perm_codename.split('.')
        except ValueError as e:
            raise ValueError(
                f"Permission codename must be in 'app_label.codename' format. Got: {perm_codename}"
            ) from e

        return self.permissions.filter(content_type__app_label=app_label, codename=codename).exists()

    def get_all_permissions(self):
        """Returns a set of all permission codenames granted by this role."""
        if not self.is_active:
            return set()

        return {
            f"{p.content_type.app_label}.{p.codename}"
            for p in self.permissions.all()
        }

class UserSetting(BaseModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                related_name='user_settings')
    dark_mode_enabled = models.BooleanField(default=False,
                                            help_text=_("Enable dark mode for the user interface."))
    email_notifications_enabled = models.BooleanField(default=True,
                                help_text=_("Receive email notifications for system events."))
    
    preferred_currency = models.ForeignKey(
        'accounting.Currency',
        on_delete=models.SET_NULL, null=True, blank=True,
        help_text=_("The user's preferred currency for display and transactions.")
    )
    
    extra_preferences = models.JSONField(default=dict, blank=True,
                        help_text=_("A JSON field to store miscellaneous user preferences."))

    class Meta:
        verbose_name = _('user setting')
        verbose_name_plural = _('user settings')

    def __str__(self):
        return f"Settings for {self.user.username}"
    def get_extra_preference(self, key, default=None):
        return self.extra_preferences.get(key, default)
    def set_extra_preference(self, key, value):
        if not isinstance(self.extra_preferences, dict):
            self.extra_preferences = {}
        self.extra_preferences[key] = value
        self.save()