"""API tests for merged local + external party search."""

from __future__ import annotations

from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import override_settings
from rest_framework.test import APITestCase

from apps.companies.models.models import Company, CompanyBranch
from apps.individuals.models.models import Individual

User = get_user_model()

REGISTRY_SETTINGS = {
    "EXTERNAL_REGISTRY_BASE_URL": "https://registry.example.com/api",
    "EXTERNAL_REGISTRY_USERNAME": "lookup-user",
    "EXTERNAL_REGISTRY_TOKEN": "lookup-token",
    "EXTERNAL_REGISTRY_TIMEOUT": 5,
}


@override_settings(**REGISTRY_SETTINGS)
class IndividualSearchMergeAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="searcher",
            email="searcher@test.com",
            password="pass",
            is_staff=True,
        )
        self.client.force_authenticate(user=self.user)
        self.local = Individual.objects.create(
            first_name="Local",
            last_name="Match",
            identification_type="national_id",
            identification_number="082047823Q29",
        )

    @patch("apps.individuals.api.views.ExternalRegistryClient")
    def test_name_search_returns_local_only(self, mock_client_cls):
        mock_client_cls.return_value.is_configured = True
        response = self.client.get("/api/individuals/search/", {"q": "Local"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["id"], self.local.id)
        mock_client_cls.return_value.search_individuals.assert_not_called()

    @patch("apps.individuals.api.views.ExternalRegistryClient")
    def test_id_search_merges_distinct_external(self, mock_client_cls):
        mock_client = mock_client_cls.return_value
        mock_client.is_configured = True
        mock_client.search_individuals.return_value = [
            {
                "id": None,
                "source": "external",
                "external_reference": "12345678A12",
                "first_name": "JANE",
                "last_name": "DOE",
                "identification_number": "12345678A12",
                "phone": "779891166",
            }
        ]

        # Local also matches via last_name/first_name? Use ID that won't hit local name filter.
        # Searching 12345678A12 won't match local 082047823Q29.
        response = self.client.get(
            "/api/individuals/search/", {"q": "12-345678-A-12"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["source"], "external")
        mock_client.search_individuals.assert_called_once_with("12345678A12")

    @patch("apps.individuals.api.views.ExternalRegistryClient")
    def test_id_search_does_not_duplicate_same_local_id(self, mock_client_cls):
        mock_client = mock_client_cls.return_value
        mock_client.is_configured = True
        mock_client.search_individuals.return_value = [
            {
                "id": None,
                "source": "external",
                "external_reference": "082047823Q29",
                "first_name": "REMOTE",
                "last_name": "DUP",
                "identification_number": "082047823Q29",
            }
        ]

        response = self.client.get(
            "/api/individuals/search/", {"q": "08-2047823-Q-29"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["id"], self.local.id)


@override_settings(**REGISTRY_SETTINGS)
class CompanySearchMergeAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="co-searcher",
            email="co@test.com",
            password="pass",
            is_staff=True,
        )
        self.client.force_authenticate(user=self.user)
        self.company = Company.objects.create(
            registration_number="99/99",
            registration_name="Other Co",
            trading_name="Other Co",
            legal_status="private",
        )
        self.branch = CompanyBranch.objects.create(
            company=self.company,
            branch_name="Other Co",
            is_headquarters=True,
        )

    @patch("apps.companies.api.views.ExternalRegistryClient")
    def test_company_search_merges_local_and_external(self, mock_client_cls):
        mock_client = mock_client_cls.return_value
        mock_client.is_configured = True
        mock_client.search_companies.return_value = [
            {
                "id": None,
                "source": "external",
                "external_reference": "FNC-000000084842",
                "branch_name": "fincheck",
                "company": {
                    "id": None,
                    "source": "external",
                    "external_reference": "FNC-000000084842",
                    "registration_number": "22/75",
                    "registration_name": "fincheck",
                    "trading_name": None,
                },
            }
        ]

        # "Co" matches local "Other Co"; external is distinct
        response = self.client.get("/api/companies/branches/search/", {"q": "Co"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["id"], self.branch.id)
        self.assertEqual(data[1]["source"], "external")

    @patch("apps.companies.api.views.ExternalRegistryClient")
    def test_company_search_keeps_external_despite_matching_name(self, mock_client_cls):
        self.company.registration_number = "99/99"
        self.company.registration_name = "fincheck"
        self.company.trading_name = "fincheck"
        self.company.save()
        self.branch.branch_name = "fincheck"
        self.branch.save()

        mock_client = mock_client_cls.return_value
        mock_client.is_configured = True
        mock_client.search_companies.return_value = [
            {
                "id": None,
                "source": "external",
                "external_reference": "FNC-000000084842",
                "branch_name": "fincheck",
                "company": {
                    "registration_number": "22/75",
                    "registration_name": "fincheck",
                    "external_reference": "FNC-000000084842",
                },
            }
        ]

        response = self.client.get("/api/companies/branches/search/", {"q": "fincheck"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["id"], self.branch.id)
        self.assertEqual(data[1]["source"], "external")

    @patch("apps.companies.api.views.ExternalRegistryClient")
    def test_company_search_dedupes_registration_number(self, mock_client_cls):
        self.company.registration_number = "22/75"
        self.company.registration_name = "fincheck"
        self.company.trading_name = "fincheck"
        self.company.save()
        self.branch.branch_name = "fincheck"
        self.branch.save()

        mock_client = mock_client_cls.return_value
        mock_client.is_configured = True
        mock_client.search_companies.return_value = [
            {
                "id": None,
                "source": "external",
                "external_reference": "FNC-000000084842",
                "branch_name": "fincheck",
                "company": {
                    "registration_number": "22/75",
                    "registration_name": "fincheck",
                    "external_reference": "FNC-000000084842",
                },
            }
        ]

        response = self.client.get("/api/companies/branches/search/", {"q": "fincheck"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["id"], self.branch.id)
