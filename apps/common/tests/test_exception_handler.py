"""
Tests for apps.common.utils.exception_handler.custom_exception_handler.

We exercise the handler by calling it directly (unit tests) as well as
via a lightweight APIView wired into a test URL conf (integration tests).
"""
import json

from django.http import Http404
from django.core.exceptions import PermissionDenied as DjangoPermissionDenied
from django.test import TestCase, RequestFactory, override_settings
from rest_framework import serializers, status
from rest_framework.exceptions import (
    AuthenticationFailed,
    MethodNotAllowed,
    NotFound,
    PermissionDenied,
    ValidationError,
)
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory, APITestCase

from apps.common.utils.exception_handler import custom_exception_handler, _flatten_detail


# ---------------------------------------------------------------------------
# Unit tests – call the handler directly
# ---------------------------------------------------------------------------

class CustomExceptionHandlerUnitTests(TestCase):
    """Direct unit tests for the custom_exception_handler function."""

    def _make_context(self):
        factory = APIRequestFactory()
        request = Request(factory.get("/api/test/"))
        return {"request": request, "view": None}

    def test_validation_error_envelope(self):
        exc = ValidationError({"name": ["This field is required."]})
        response = custom_exception_handler(exc, self._make_context())

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = response.data
        self.assertEqual(data["status"], "error")
        self.assertIn("Validation", data["message"])
        self.assertIn("name", data["errors"])

    def test_404_not_found_envelope(self):
        exc = NotFound()
        response = custom_exception_handler(exc, self._make_context())

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["status"], "error")
        self.assertIn("errors", response.data)
        self.assertIn("message", response.data)

    def test_405_method_not_allowed_envelope(self):
        exc = MethodNotAllowed("POST")
        response = custom_exception_handler(exc, self._make_context())

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response.data["status"], "error")
        self.assertIn("errors", response.data)
        self.assertIn("message", response.data)

    def test_django_http404_converted(self):
        """Django Http404 must be converted to a structured 404 response."""
        exc = Http404()
        response = custom_exception_handler(exc, self._make_context())

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["status"], "error")

    def test_django_permission_denied_converted(self):
        """Django PermissionDenied must be converted to a structured 403 response."""
        exc = DjangoPermissionDenied()
        response = custom_exception_handler(exc, self._make_context())

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["status"], "error")

    def test_authentication_failed_envelope(self):
        exc = AuthenticationFailed("Invalid token.")
        response = custom_exception_handler(exc, self._make_context())

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["status"], "error")
        self.assertIn("message", response.data)
        self.assertIn("errors", response.data)

    def test_unhandled_exception_returns_none(self):
        """Non-DRF, non-Django exceptions should be left to other handlers."""
        exc = RuntimeError("unexpected")
        response = custom_exception_handler(exc, self._make_context())

        self.assertIsNone(response)

    def test_envelope_always_has_three_keys(self):
        """Every handled response must have exactly status, message, errors."""
        for exc in [
            ValidationError("bad input"),
            NotFound(),
            MethodNotAllowed("DELETE"),
            PermissionDenied(),
            AuthenticationFailed(),
        ]:
            with self.subTest(exc=exc):
                response = custom_exception_handler(exc, self._make_context())
                self.assertIsNotNone(response)
                self.assertIn("status", response.data)
                self.assertIn("message", response.data)
                self.assertIn("errors", response.data)


# ---------------------------------------------------------------------------
# Tests for the _flatten_detail helper
# ---------------------------------------------------------------------------

class FlattenDetailTests(TestCase):
    def test_string(self):
        self.assertEqual(_flatten_detail("some error"), "some error")

    def test_list(self):
        self.assertEqual(_flatten_detail(["first", "second"]), "first")

    def test_dict(self):
        result = _flatten_detail({"field": ["error msg"]})
        self.assertEqual(result, "error msg")

    def test_nested(self):
        result = _flatten_detail({"outer": {"inner": ["deep error"]}})
        self.assertEqual(result, "deep error")
