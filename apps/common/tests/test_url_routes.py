"""
Smoke tests to verify all app URL namespaces are reachable.

Each list endpoint should return 200 (if public) or 401/403 (if authentication
is required) – never 404.  A 404 would indicate a URL route is missing.
"""

from django.test import TestCase


class AppURLSmokeTest(TestCase):
    """Verify that every app's root API endpoint is reachable."""

    ENDPOINTS = [
        "/api/auth/",
        "/api/individuals/",
        "/api/companies/",
        "/api/clients/",
        "/api/asset-management/",
        "/api/hire-purchase/",
        "/api/collateral/",
        "/api/common/",
    ]

    def test_all_endpoints_reachable(self):
        """All registered API endpoints must return 200, 401, or 403 – not 404."""
        for endpoint in self.ENDPOINTS:
            with self.subTest(endpoint=endpoint):
                response = self.client.get(endpoint)
                self.assertIn(
                    response.status_code,
                    (200, 401, 403),
                    msg=(
                        f"Endpoint {endpoint!r} returned HTTP {response.status_code}. "
                        "Expected 200, 401, or 403. A 404 means the URL route is missing."
                    ),
                )
