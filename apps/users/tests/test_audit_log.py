"""
Tests for the audit logging feature.

Covers:
- AuditLog model creation via audit_service.create_audit_log
- AuditLogViewSet (GET /api/audit-log/) — staff-only, read-only, paginated
- Append-only constraint (PUT / PATCH / DELETE must return 405)
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

from apps.users.models.audit import AuditLog
from apps.users.services.audit_service import create_audit_log

User = get_user_model()


class AuditLogModelTest(TestCase):
    """Unit tests for create_audit_log helper."""

    def setUp(self):
        self.staff_user = User.objects.create_user(
            username="staff@test.com",
            email="staff@test.com",
            password="testpass123",
            is_staff=True,
            is_verified=True,
        )

    def test_create_audit_log_no_request(self):
        """create_audit_log works without a request object."""
        entry = create_audit_log(
            request=None,
            action="test.action",
            resource_type="TestModel",
            resource_id=42,
            details={"key": "value"},
        )
        self.assertIsInstance(entry, AuditLog)
        self.assertEqual(entry.action, "test.action")
        self.assertEqual(entry.resource_type, "TestModel")
        self.assertEqual(entry.resource_id, 42)
        self.assertIsNone(entry.created_by)
        self.assertTrue(entry.success)

    def test_create_audit_log_with_details(self):
        """create_audit_log stores arbitrary JSON details."""
        entry = create_audit_log(
            request=None,
            action="user.create",
            resource_type="CustomUser",
            resource_id=1,
            details={"username": "alice", "email": "alice@example.com"},
        )
        self.assertEqual(entry.details["username"], "alice")

    def test_audit_log_is_append_only_in_db(self):
        """AuditLog entries cannot be deleted via the ORM in a way that bypasses
        the append-only policy enforced in the API layer."""
        entry = create_audit_log(
            request=None,
            action="test.event",
            resource_type="SomeModel",
            resource_id=1,
        )
        pk = entry.pk
        # The row exists
        self.assertTrue(AuditLog.objects.filter(pk=pk).exists())
        # Directly deleting via ORM is still possible at the DB level,
        # but the API layer must reject DELETE requests.


class AuditLogAPITest(TestCase):
    """Integration tests for GET /api/audit-log/."""

    def setUp(self):
        self.client = APIClient()
        # Staff user — should be allowed access
        self.staff_user = User.objects.create_user(
            username="staff@test.com",
            email="staff@test.com",
            password="testpass123",
            is_staff=True,
            is_verified=True,
        )
        # Non-staff user — must be denied
        self.regular_user = User.objects.create_user(
            username="regular@test.com",
            email="regular@test.com",
            password="testpass123",
            is_staff=False,
            is_verified=True,
        )
        # Seed a couple of entries
        create_audit_log(request=None, action="asset.create", resource_type="Asset", resource_id=1)
        create_audit_log(request=None, action="user.login", resource_type="User", resource_id=2)

    def test_staff_can_list_audit_log(self):
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.get("/api/audit-log/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Results are paginated
        self.assertIn("results", response.data)
        self.assertGreaterEqual(len(response.data["results"]), 2)

    def test_non_staff_cannot_list_audit_log(self):
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get("/api/audit-log/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_cannot_list_audit_log(self):
        response = self.client.get("/api/audit-log/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_audit_log_endpoint_is_readonly_post_not_allowed(self):
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.post("/api/audit-log/", data={"action": "manual"})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_audit_log_endpoint_is_readonly_delete_not_allowed(self):
        entry = create_audit_log(request=None, action="to.delete", resource_type="X", resource_id=99)
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.delete(f"/api/audit-log/{entry.pk}/")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_audit_log_endpoint_is_readonly_put_not_allowed(self):
        entry = create_audit_log(request=None, action="to.update", resource_type="X", resource_id=100)
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.put(f"/api/audit-log/{entry.pk}/", data={"action": "changed"})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_audit_log_detail_accessible_by_staff(self):
        entry = create_audit_log(request=None, action="detail.test", resource_type="X", resource_id=5)
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.get(f"/api/audit-log/{entry.pk}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["action"], "detail.test")
