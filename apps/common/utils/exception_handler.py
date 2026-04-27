import logging

from django.core.exceptions import PermissionDenied
from django.http import Http404
from rest_framework import exceptions, status
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Custom DRF exception handler that wraps all error responses in a
    consistent envelope::

        {
            "status": "error",
            "message": "<human-readable summary>",
            "errors": { ... }   # field-level detail, may be empty
        }

    The handler delegates to the default DRF handler first so that
    authentication, throttling and permission responses are still
    generated correctly, then it re-shapes the response body.

    Django's ``Http404`` and ``PermissionDenied`` exceptions are
    converted to the appropriate DRF equivalents before the default
    handler runs (mirroring the behaviour of
    ``rest_framework.views.set_rollback``).
    """
    # Let Django's Http404 / PermissionDenied be handled by DRF
    if isinstance(exc, Http404):
        exc = exceptions.NotFound()
    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    response = drf_exception_handler(exc, context)

    if response is None:
        # Unhandled exception – do not interfere; Django / middleware will deal with it.
        return None

    # --- Build the consistent envelope ---
    original_data = response.data

    # Extract a top-level human-readable message
    if isinstance(exc, exceptions.ValidationError):
        message = "Validation failed. Please correct the errors and try again."
    else:
        # Use DRF's built-in `detail` attribute when available
        detail = getattr(exc, "detail", None)
        if detail is not None:
            message = _flatten_detail(detail)
        else:
            message = str(exc)

    # Build the `errors` dict – keep field-level detail intact when present
    if isinstance(original_data, dict):
        errors = original_data
    elif isinstance(original_data, list):
        errors = {"non_field_errors": original_data}
    else:
        errors = {}

    response.data = {
        "status": "error",
        "message": message,
        "errors": errors,
    }

    return response


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _flatten_detail(detail):
    """
    Recursively extract the first human-readable string from a DRF
    ``detail`` value (which may be a string, list, or dict).
    """
    if isinstance(detail, dict):
        for value in detail.values():
            return _flatten_detail(value)
    if isinstance(detail, list) and detail:
        return _flatten_detail(detail[0])
    return str(detail)
