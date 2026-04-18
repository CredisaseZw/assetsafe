"""Tests for individual document upload and management endpoints.

Covers:
    - GET  /api/individuals/{id}/documents/   → list documents
    - POST /api/individuals/{id}/documents/   → upload document (201)
    - DELETE /api/individuals/{id}/documents/{doc_id}/ → delete document (204)
    - Files over 10 MB → 400
    - Unauthenticated requests → 401
    - Cross-client upload attempts → 403
"""

import io
import os
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase, override_settings
from rest_framework import status
from rest_framework.test import APIClient

from apps.common.models.models import Document
from apps.individuals.models.models import Individual
from apps.users.models.models import CustomUser


def _make_individual(**kwargs):
    defaults = dict(
        first_name="Test",
        last_name="User",
        identification_type="passport",
        identification_number=kwargs.pop("identification_number", "AB123456"),
    )
    defaults.update(kwargs)
    return Individual.objects.create(**defaults)


def _make_staff_user(username="staffuser"):
    user = CustomUser.objects.create_user(
        username=username,
        password="testpass123",
        email=f"{username}@example.com",
        is_staff=True,
    )
    return user


def _fake_file(name="doc.pdf", content_type="application/pdf", size_bytes=1024):
    """Return an in-memory file suitable for multipart upload."""
    data = b"%PDF-1.4 " + b"x" * max(0, size_bytes - 9)
    f = io.BytesIO(data)
    f.name = name
    f.content_type = content_type
    f.size = len(data)
    return f


@override_settings(
    MEDIA_ROOT="/tmp/test_media_assetsafe",
    DEFAULT_FILE_STORAGE="django.core.files.storage.FileSystemStorage",
)
class IndividualDocumentTests(TestCase):
    def setUp(self):
        self.client_api = APIClient()
        self.staff_user = _make_staff_user()
        self.individual = _make_individual(identification_number="TESTPASS001")
        self.url_list = f"/api/individuals/{self.individual.pk}/documents/"

    def _doc_url(self, doc_id):
        return f"/api/individuals/{self.individual.pk}/documents/{doc_id}/"

    # ------------------------------------------------------------------
    # Authentication guard
    # ------------------------------------------------------------------

    def test_list_requires_authentication(self):
        response = self.client_api.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_upload_requires_authentication(self):
        f = _fake_file()
        response = self.client_api.post(
            self.url_list, {"file": f, "document_type": "id"}, format="multipart"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # ------------------------------------------------------------------
    # GET – list documents
    # ------------------------------------------------------------------

    def test_list_empty(self):
        self.client_api.force_authenticate(user=self.staff_user)
        response = self.client_api.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), [])

    def test_list_with_existing_document(self):
        individual_ct = ContentType.objects.get_for_model(self.individual)
        doc = Document.objects.create(
            content_type=individual_ct,
            object_id=self.individual.pk,
            document_type="id",
            file="documents/test_doc.pdf",
        )
        self.client_api.force_authenticate(user=self.staff_user)
        response = self.client_api.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["id"], doc.pk)
        self.assertIn("document_type", data[0])
        self.assertIn("file_url", data[0])

    # ------------------------------------------------------------------
    # POST – upload a document
    # ------------------------------------------------------------------

    def test_upload_valid_pdf(self):
        self.client_api.force_authenticate(user=self.staff_user)
        f = _fake_file(name="contract.pdf", content_type="application/pdf")
        response = self.client_api.post(
            self.url_list,
            {"file": f, "document_type": "contract"},
            format="multipart",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.json()
        self.assertIn("id", data)
        self.assertEqual(data["document_type"], "contract")
        self.assertIn("file_url", data)
        # Ensure it was actually saved
        self.assertTrue(
            Document.objects.filter(
                pk=data["id"],
                object_id=self.individual.pk,
            ).exists()
        )

    def test_upload_valid_jpeg(self):
        self.client_api.force_authenticate(user=self.staff_user)
        f = _fake_file(name="photo.jpg", content_type="image/jpeg")
        response = self.client_api.post(
            self.url_list,
            {"file": f, "document_type": "id"},
            format="multipart",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_upload_file_too_large_returns_400(self):
        self.client_api.force_authenticate(user=self.staff_user)
        # Just over 10 MB
        f = _fake_file(
            name="big.pdf",
            content_type="application/pdf",
            size_bytes=10 * 1024 * 1024 + 1,
        )
        response = self.client_api.post(
            self.url_list,
            {"file": f, "document_type": "other"},
            format="multipart",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.json())

    def test_upload_disallowed_mime_type_returns_400(self):
        self.client_api.force_authenticate(user=self.staff_user)
        f = _fake_file(name="script.exe", content_type="application/octet-stream")
        response = self.client_api.post(
            self.url_list,
            {"file": f, "document_type": "other"},
            format="multipart",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.json())

    def test_upload_missing_document_type_returns_400(self):
        self.client_api.force_authenticate(user=self.staff_user)
        f = _fake_file()
        response = self.client_api.post(
            self.url_list, {"file": f}, format="multipart"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_upload_to_nonexistent_individual_returns_404(self):
        self.client_api.force_authenticate(user=self.staff_user)
        f = _fake_file()
        url = "/api/individuals/999999/documents/"
        response = self.client_api.post(
            url, {"file": f, "document_type": "id"}, format="multipart"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # ------------------------------------------------------------------
    # DELETE – remove a document
    # ------------------------------------------------------------------

    def test_delete_document(self):
        individual_ct = ContentType.objects.get_for_model(self.individual)
        doc = Document.objects.create(
            content_type=individual_ct,
            object_id=self.individual.pk,
            document_type="id",
            file="documents/delete_me.pdf",
        )
        self.client_api.force_authenticate(user=self.staff_user)
        response = self.client_api.delete(self._doc_url(doc.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Document.objects.filter(pk=doc.pk).exists())

    def test_delete_nonexistent_document_returns_404(self):
        self.client_api.force_authenticate(user=self.staff_user)
        response = self.client_api.delete(self._doc_url(999999))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_document_belonging_to_another_individual(self):
        other_individual = _make_individual(identification_number="TESTPASS002")
        other_ct = ContentType.objects.get_for_model(other_individual)
        doc = Document.objects.create(
            content_type=other_ct,
            object_id=other_individual.pk,
            document_type="contract",
            file="documents/other.pdf",
        )
        self.client_api.force_authenticate(user=self.staff_user)
        # Trying to delete via the first individual's URL should return 404
        response = self.client_api.delete(self._doc_url(doc.pk))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        # Original document should still exist
        self.assertTrue(Document.objects.filter(pk=doc.pk).exists())

    # ------------------------------------------------------------------
    # Same-client permission check
    # ------------------------------------------------------------------

    def test_non_staff_user_from_different_client_is_forbidden(self):
        """A non-staff user whose client is not linked to the target
        individual should receive 403."""
        from apps.clients.models.models import Client

        # Create a second individual that will be the "other user's" client target
        other_individual = _make_individual(identification_number="TESTPASS003")
        other_ct = ContentType.objects.get_for_model(other_individual)

        other_client = Client.objects.create(
            client_content_type=other_ct,
            client_object_id=other_individual.pk,
        )
        non_staff_user = CustomUser.objects.create_user(
            username="nonstaffuser",
            password="testpass123",
            email="nonstaff@example.com",
            is_staff=False,
            client=other_client,
        )
        self.client_api.force_authenticate(user=non_staff_user)

        # Try to list documents for the *first* individual
        response = self.client_api.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_non_staff_user_for_same_client_can_upload(self):
        """A non-staff user whose client IS linked to the target individual
        should be able to upload."""
        from apps.clients.models.models import Client

        individual_ct = ContentType.objects.get_for_model(self.individual)
        own_client = Client.objects.create(
            client_content_type=individual_ct,
            client_object_id=self.individual.pk,
        )
        same_client_user = CustomUser.objects.create_user(
            username="sameclientuser",
            password="testpass123",
            email="sameclient@example.com",
            is_staff=False,
            client=own_client,
        )
        self.client_api.force_authenticate(user=same_client_user)

        f = _fake_file(name="id.pdf", content_type="application/pdf")
        response = self.client_api.post(
            self.url_list,
            {"file": f, "document_type": "id"},
            format="multipart",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
