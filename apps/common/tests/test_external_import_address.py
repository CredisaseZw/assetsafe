"""Tests for external party import address persistence."""

from __future__ import annotations

from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase, override_settings

from apps.common.models.models import Address
from apps.companies.models.models import CompanyBranch
from apps.companies.services.external_import import import_external_company
from apps.individuals.models.models import Individual
from apps.individuals.services.external_import import import_external_individual

User = get_user_model()

REGISTRY_SETTINGS = {
    "EXTERNAL_REGISTRY_BASE_URL": "https://registry.example.com/api",
    "EXTERNAL_REGISTRY_USERNAME": "lookup-user",
    "EXTERNAL_REGISTRY_TOKEN": "lookup-token",
    "EXTERNAL_REGISTRY_TIMEOUT": 5,
}

COMPANY_MAPPED = {
    "id": None,
    "source": "external",
    "external_reference": "22/75",
    "branch_name": "fincheck",
    "is_headquarters": True,
    "email": "info@fincheck.test",
    "phone": "771234567",
    "_street_address": "club chambers",
    "company": {
        "registration_number": "22/75",
        "registration_name": "fincheck",
        "trading_name": None,
        "external_reference": "FNC-000000084842",
    },
}

PERSON_MAPPED = {
    "id": None,
    "source": "external",
    "external_reference": "12345678A12",
    "first_name": "JANE",
    "last_name": "DOE",
    "identification_number": "12345678A12",
    "phone": "779891166",
    "email": None,
    "_street_address": "5813 GOLFCOURSE MZARI, CHINHOYI",
}


@override_settings(**REGISTRY_SETTINGS)
class ExternalCompanyImportAddressTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="importer",
            email="importer@test.com",
            password="pass",
            is_staff=True,
        )

    @patch("apps.companies.services.external_import.ExternalRegistryClient")
    def test_import_persists_current_address_as_street_address(self, mock_client_cls):
        mock_client_cls.return_value.get_company_branch.return_value = COMPANY_MAPPED

        branch = import_external_company("22/75", created_by=self.user)

        self.assertIsInstance(branch, CompanyBranch)
        self.assertEqual(branch.email, "info@fincheck.test")
        self.assertEqual(branch.phone, "771234567")

        ct = ContentType.objects.get_for_model(CompanyBranch)
        address = Address.objects.filter(
            content_type=ct,
            object_id=branch.pk,
            address_type="physical",
            is_primary=True,
        ).first()
        self.assertIsNotNone(address)
        self.assertEqual(address.street_address, "club chambers")
        self.assertIsNone(address.suburb_id)


@override_settings(**REGISTRY_SETTINGS)
class ExternalIndividualImportAddressTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="person-importer",
            email="person@test.com",
            password="pass",
            is_staff=True,
        )

    @patch("apps.individuals.services.external_import.ExternalRegistryClient")
    def test_import_persists_address_as_street_address(self, mock_client_cls):
        mock_client_cls.return_value.get_individual.return_value = PERSON_MAPPED

        individual = import_external_individual(
            "12345678A12", created_by=self.user
        )

        self.assertIsInstance(individual, Individual)
        self.assertEqual(individual.identification_number, "12345678A12")

        ct = ContentType.objects.get_for_model(Individual)
        address = Address.objects.filter(
            content_type=ct,
            object_id=individual.pk,
            address_type="physical",
            is_primary=True,
        ).first()
        self.assertIsNotNone(address)
        self.assertEqual(
            address.street_address, "5813 GOLFCOURSE MZARI, CHINHOYI"
        )

    @patch("apps.individuals.services.external_import.ExternalRegistryClient")
    def test_import_backfills_address_on_existing(self, mock_client_cls):
        existing = Individual.objects.create(
            first_name="JANE",
            last_name="DOE",
            identification_type="national_id",
            identification_number="12345678A12",
            external_reference="12345678A12",
            source="external",
        )
        mock_client_cls.return_value.get_individual.return_value = PERSON_MAPPED

        individual = import_external_individual(
            "12345678A12", created_by=self.user
        )

        self.assertEqual(individual.pk, existing.pk)
        ct = ContentType.objects.get_for_model(Individual)
        address = Address.objects.filter(
            content_type=ct,
            object_id=individual.pk,
            is_primary=True,
        ).first()
        self.assertIsNotNone(address)
        self.assertEqual(
            address.street_address, "5813 GOLFCOURSE MZARI, CHINHOYI"
        )
