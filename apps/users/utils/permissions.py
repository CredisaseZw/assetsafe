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

    message = _(
        "You do not have permission to create users for this company or you are not associated with a company."
    )

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        # Superusers and staff users always have permission
        if request.user.is_superuser or request.user.is_staff:
            return True

        # Check for Django's built-in 'add_customuser' permission
        if not request.user.has_perm("users.add_customuser"):
            return False

        # Ensuring the creating user is associated with a company
        admin_company = request.user.get_associated_company()
        if not admin_company:
            self.message = _(
                "You must be associated with a company to create users for it."
            )
            return False

        return True


class HasRole(permissions.BasePermission):
    """
    Allows access only to users who have a specific role.
    Usage:
        class MyView(APIView):
            permission_classes = [HasRole]
            required_roles = ['admin', 'financier']
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        required_roles = getattr(view, "required_roles", [])
        if not required_roles:
            return True

        if request.user.is_superuser:
            return True

        return request.user.roles.filter(name__in=required_roles).exists()


class IsSuperuser(permissions.BasePermission):
    """Allows access only to Django superusers."""

    message = _("You must be a superuser to access this resource.")

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_superuser
        )


class IsVerified(permissions.BasePermission):
    """
    Allows access only to verified users.
    """

    message = _("Your account must be verified to access this resource.")

    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and request.user.is_verified
        )


def roles_allowed(roles):
    def decorator(func):
        func.required_roles = roles
        return func

    return decorator
