from __future__ import annotations

from django.db.models import QuerySet
from rest_framework.exceptions import ValidationError

CLIENT_ROLE_NAMES: tuple[str, ...] = (
    "client_user",
    "client_admin",
    "individual_client",
    "company_client",
)


def scope_registry_to_client_portfolio(
    queryset: QuerySet, user, *, financier_field: str = "financier_id"
):
    """
    Limit client-role users to records where their organisation is the
    financier.  Staff/admin users without those roles see the full registry.

    Both list and stats endpoints must call this helper so headline counts
    never disagree with the table below.
    """
    if (
        user.is_authenticated
        and user.client_id
        and user.roles.filter(name__in=CLIENT_ROLE_NAMES).exists()
    ):
        return queryset.filter(**{financier_field: user.client_id})
    return queryset


def extract_error_message(error):
    """
    Recursively extract the first human-readable error message
    from the Validation Error.
    """
    if isinstance(error, ValidationError):
        detail = error.detail
    else:
        detail = error

    # Dict: go into the first value
    if isinstance(detail, dict):
        for value in detail.values():
            return extract_error_message(value)

    # List: go into the first item
    if isinstance(detail, list) and detail:
        return extract_error_message(detail[0])

    # ErrorDetail or string
    return str(detail)
