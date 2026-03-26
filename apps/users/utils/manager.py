# myauthapp/manager.py
from django.contrib.auth.models import BaseUserManager
from django.db import IntegrityError, transaction
from django.utils.translation import gettext_lazy as _

def generate_unique_username(prefix_letters, instance_id, length=5):
    """Generates a unique username in a specific format (e.g., 'A0001')."""
    zeros = (length - len(prefix_letters) - len(str(instance_id))) * "0"
    return f"{prefix_letters}{zeros}{instance_id}"


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifier
    for authentication instead of usernames.
    """
    def create_user(self, username, email=None, password=None, **extra_fields):
        """
        Create and save a User with the given username, email and password.
        """
        if not username:
            raise ValueError(_('The Username must be set'))
        
        if email:
            email = self.normalize_email(email)

        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        
        with transaction.atomic():
            user.save(using=self._db) # Initial save to get PK
            if not user.username: # If username was not provided and needs generation
                user.username = user._generate_unique_username_from_pk() # Call helper method
                user.save(update_fields=['username'], using=self._db) # Save again with username
        
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        """
        Create and save a SuperUser with the given username, email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        
        return self.create_user(username, email, password, **extra_fields)

    def _generate_unique_username_from_pk(self, instance_pk):
        """Generates a unique username for a given instance PK."""
        return generate_unique_username('U', instance_pk, length=8)