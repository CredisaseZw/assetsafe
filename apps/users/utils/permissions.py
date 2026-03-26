# users/permissions.py

from rest_framework import permissions
from django.utils.translation import gettext_lazy as _

class CanCreateCompanyUsers(permissions.BasePermission):
    """
    Custom permission to only allow:
    1. Superusers/Staff users.
    2. Users with 'users.add_customuser' permission AND a linked Company (as determined by get_associated_company),
    to create users for their own associated company.
    """
    message = _("You do not have permission to create users for this company or you are not associated with a company.")

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        # Superusers and staff users always have permission
        if request.user.is_superuser or request.user.is_staff:
            return True

        # Check for Django's built-in 'add_customuser' permission
        if not request.user.has_perm('users.add_customuser'):
            return False

        # Ensuring the creating user is associated with a company
        admin_company = request.user.get_associated_company()
        if not admin_company:
            self.message = _("You must be associated with a company to create users for it.")
            return False

        return True