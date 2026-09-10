"""Tests for external lookup-person / lookup-company client."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from django.test import SimpleTestCase, override_settings

from apps.common.services.external_registry import (
    ExternalRegistryClient,
    looks_like_national_id,
    merge_company_search_results,
    merge_individual_search_results,
    normalize_national_id,
    primary_address_from_street,
)

PERSON_PAYLOAD = {
    "found": True,
    "individual": {
        "fins_number": "12345678A12",
        "national_id": "12345678A12",
        "firstname": "JANE",
        "surname": "DOE",
        "dob": None,
        "gender": None,
        "mobile": "779891166",
        "address": "5813 GOLFCOURSE MZARI, CHINHOYI",
        "risk_class": None,
    },
    "summary": {"claims_count": 1, "court_cases_count": 0},
    "claims": [],
    "court_records": [],
}

COMPANY_PAYLOAD = {
    "found": True,
    "company": {
        "fins_number": "FNC-000000084842",
        "registration_number": "22/75",
        "registration_name": "fincheck",
        "trading_name": None,
        "mobile_phone": "",
        "email": None,
        "current_address": "club chambers",
        "industry": None,
        "risk_class": None,
        "legal_status": None,
        "trading_status": None,
    },
    "summary": {"claims_count": 2, "court_cases_count": 0},
    "claims": [],
    "court_records": [],
}

REGISTRY_SETTINGS = {
    "EXTERNAL_REGISTRY_BASE_URL": "https://registry.example.com/api",
    "EXTERNAL_REGISTRY_USERNAME": "lookup-user",
    "EXTERNAL_REGISTRY_TOKEN": "lookup-token",
    "EXTERNAL_REGISTRY_TIMEOUT": 5,
}


class LooksLikeNationalIdTests(SimpleTestCase):
    def test_accepts_zimbabwe_style_id(self):
        # 11-char compact (2+6+letter+2)
        self.assertTrue(looks_like_national_id("12345678A12"))
        self.assertTrue(looks_like_national_id("12345678a12"))
        self.assertTrue(looks_like_national_id("12-345678-A-12"))
        self.assertTrue(looks_like_national_id("12 345678 A 12"))
        # 12-char compact (2+7+letter+2)
        self.assertTrue(looks_like_national_id("082047823Q29"))
        self.assertTrue(looks_like_national_id("08-2047823-Q-29"))
        self.assertTrue(looks_like_national_id("08-2047823Q29"))

    def test_normalize_strips_separators(self):
        self.assertEqual(normalize_national_id("12-345678-A-12"), "12345678A12")
        self.assertEqual(normalize_national_id("08-2047823-Q-29"), "082047823Q29")
        self.assertEqual(normalize_national_id("12345678a12"), "12345678A12")

    def test_rejects_names(self):
        self.assertFalse(looks_like_national_id("Jane"))
        self.assertFalse(looks_like_national_id("Jane Doe"))
        self.assertFalse(looks_like_national_id(""))
        self.assertFalse(looks_like_national_id("22/75"))


class MergeSearchResultsTests(SimpleTestCase):
    def test_merge_individuals_prefers_local_and_dedupes_same_id(self):
        local = [
            {
                "id": 1,
                "first_name": "Local",
                "last_name": "Person",
                "identification_number": "12345678A12",
                "source": "internal",
                "external_reference": None,
            }
        ]
        external = [
            {
                "id": None,
                "first_name": "JANE",
                "last_name": "DOE",
                "identification_number": "12345678A12",
                "source": "external",
                "external_reference": "12345678A12",
            }
        ]
        merged = merge_individual_search_results(local, external)
        self.assertEqual(len(merged), 1)
        self.assertEqual(merged[0]["id"], 1)

    def test_merge_individuals_keeps_distinct_external(self):
        local = [
            {
                "id": 1,
                "identification_number": "082047823Q29",
                "external_reference": None,
            }
        ]
        external = [
            {
                "id": None,
                "identification_number": "12345678A12",
                "external_reference": "12345678A12",
                "source": "external",
            }
        ]
        merged = merge_individual_search_results(local, external)
        self.assertEqual(len(merged), 2)
        self.assertEqual(merged[0]["id"], 1)
        self.assertEqual(merged[1]["source"], "external")

    def test_merge_companies_dedupes_registration_number(self):
        local = [
            {
                "id": 10,
                "branch_name": "HQ",
                "company": {
                    "registration_number": "22/75",
                    "registration_name": "Local Fincheck",
                    "external_reference": None,
                },
            }
        ]
        external = [
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
        merged = merge_company_search_results(local, external)
        self.assertEqual(len(merged), 1)
        self.assertEqual(merged[0]["id"], 10)

    def test_merge_companies_keeps_external_when_only_names_overlap(self):
        """Same display name but different reg numbers must both appear."""
        local = [
            {
                "id": 10,
                "branch_name": "fincheck",
                "company": {
                    "registration_number": "99/99",
                    "registration_name": "fincheck",
                    "trading_name": "fincheck",
                },
            }
        ]
        external = [
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
        merged = merge_company_search_results(local, external)
        self.assertEqual(len(merged), 2)
        self.assertEqual(merged[0]["id"], 10)
        self.assertEqual(merged[1]["source"], "external")

    def test_merge_companies_appends_distinct_external(self):
        local = [
            {
                "id": 10,
                "branch_name": "Other Co",
                "company": {
                    "registration_number": "99/99",
                    "registration_name": "Other Co",
                },
            }
        ]
        external = [
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
        merged = merge_company_search_results(local, external)
        self.assertEqual(len(merged), 2)

    def test_primary_address_from_street(self):
        address = primary_address_from_street("club chambers")
        self.assertEqual(address["street_address"], "club chambers")
        self.assertEqual(address["address_type"], "physical")
        self.assertIsNone(address["suburb"])
        self.assertIsNone(primary_address_from_street(""))
        self.assertIsNone(primary_address_from_street(None))

    def test_merge_applies_address_onto_local_missing_primary_address(self):
        """Matching external hit no longer injects address into slim search rows."""
        local = [
            {
                "id": None,
                "branch_name": "fincheck",
                "company": {
                    "registration_number": "22/75",
                    "registration_name": "fincheck",
                    "external_reference": "FNC-000000084842",
                },
            }
        ]
        external = [
            {
                "branch_name": "fincheck",
                "_street_address": "club chambers",
                "external_reference": "22/75",
                "source": "external",
                "company": {
                    "registration_number": "22/75",
                    "registration_name": "fincheck",
                    "external_reference": "FNC-000000084842",
                },
            }
        ]
        merged = merge_company_search_results(local, external)
        self.assertEqual(len(merged), 1)
        self.assertNotIn("primary_address", merged[0])
        self.assertNotIn("address_summary", merged[0])


@override_settings(**REGISTRY_SETTINGS)
class ExternalRegistryClientTests(SimpleTestCase):
    def test_is_configured_requires_credentials(self):
        client = ExternalRegistryClient()
        self.assertTrue(client.is_configured)

    @override_settings(EXTERNAL_REGISTRY_TOKEN="")
    def test_not_configured_without_token(self):
        client = ExternalRegistryClient()
        self.assertFalse(client.is_configured)

    def test_headers_use_username_and_token(self):
        client = ExternalRegistryClient()
        self.assertEqual(
            client._headers(),
            {
                "Accept": "application/json",
                "Username": "lookup-user",
                "Token": "lookup-token",
            },
        )

    @patch("apps.common.services.external_registry.requests.request")
    def test_search_individuals_maps_lookup_person(self, mock_request):
        response = MagicMock()
        response.raise_for_status = MagicMock()
        response.json.return_value = PERSON_PAYLOAD
        mock_request.return_value = response

        results = ExternalRegistryClient().search_individuals("12345678A12")

        mock_request.assert_called_once()
        _, kwargs = mock_request.call_args
        self.assertEqual(
            mock_request.call_args.args[:2],
            ("GET", "https://registry.example.com/api/lookup-person/"),
        )
        self.assertEqual(kwargs["params"], {"national_id": "12345678A12"})
        self.assertEqual(kwargs["headers"]["Username"], "lookup-user")
        self.assertEqual(kwargs["headers"]["Token"], "lookup-token")

        self.assertEqual(len(results), 1)
        person = results[0]
        self.assertIsNone(person["id"])
        self.assertEqual(person["source"], "external")
        self.assertEqual(person["external_reference"], "12345678A12")
        self.assertEqual(person["first_name"], "JANE")
        self.assertEqual(person["last_name"], "DOE")
        self.assertEqual(person["identification_number"], "12345678A12")
        self.assertEqual(person["phone"], "779891166")
        self.assertEqual(
            person["_street_address"], "5813 GOLFCOURSE MZARI, CHINHOYI"
        )
        self.assertNotIn("primary_address", person)
        self.assertNotIn("is_active", person)
        self.assertNotIn("date_of_birth", person)
        self.assertNotIn("gender", person)

    @patch("apps.common.services.external_registry.requests.request")
    def test_search_individuals_skips_name_queries(self, mock_request):
        results = ExternalRegistryClient().search_individuals("Jane Doe")
        self.assertEqual(results, [])
        mock_request.assert_not_called()

    @patch("apps.common.services.external_registry.requests.request")
    def test_search_individuals_not_found(self, mock_request):
        response = MagicMock()
        response.raise_for_status = MagicMock()
        response.json.return_value = {"found": False, "individual": None}
        mock_request.return_value = response

        results = ExternalRegistryClient().search_individuals("12345678A12")
        self.assertEqual(results, [])

    @patch("apps.common.services.external_registry.requests.request")
    def test_search_companies_maps_lookup_company(self, mock_request):
        response = MagicMock()
        response.raise_for_status = MagicMock()
        response.json.return_value = COMPANY_PAYLOAD
        mock_request.return_value = response

        results = ExternalRegistryClient().search_companies("22/75")

        mock_request.assert_called_once()
        self.assertEqual(
            mock_request.call_args.args[:2],
            ("GET", "https://registry.example.com/api/lookup-company/"),
        )
        self.assertEqual(mock_request.call_args.kwargs["params"], {"search": "22/75"})

        self.assertEqual(len(results), 1)
        branch = results[0]
        self.assertIsNone(branch["id"])
        self.assertEqual(branch["source"], "external")
        self.assertEqual(branch["external_reference"], "22/75")
        self.assertEqual(branch["branch_name"], "fincheck")
        self.assertEqual(branch["company"]["registration_number"], "22/75")
        self.assertEqual(branch["company"]["registration_name"], "fincheck")
        self.assertEqual(branch["company"]["external_reference"], "FNC-000000084842")
        self.assertNotIn("legal_status", branch["company"])
        self.assertNotIn("legal_status_display", branch["company"])
        self.assertNotIn("is_verified", branch["company"])
        self.assertNotIn("fins_number", branch["company"])
        self.assertNotIn("current_address", branch)
        self.assertNotIn("current_address", branch["company"])
        self.assertNotIn("primary_address", branch)
        self.assertNotIn("address_summary", branch)
        self.assertEqual(branch["_street_address"], "club chambers")
        self.assertIsNone(branch["phone"])
        self.assertIsNone(branch["email"])

    @patch("apps.common.services.external_registry.requests.request")
    def test_search_companies_not_found(self, mock_request):
        response = MagicMock()
        response.raise_for_status = MagicMock()
        response.json.return_value = {"found": False, "company": None}
        mock_request.return_value = response

        results = ExternalRegistryClient().search_companies("missing-co")
        self.assertEqual(results, [])

    @patch("apps.common.services.external_registry.requests.request")
    def test_get_individual_uses_lookup_person(self, mock_request):
        response = MagicMock()
        response.raise_for_status = MagicMock()
        response.json.return_value = PERSON_PAYLOAD
        mock_request.return_value = response

        record = ExternalRegistryClient().get_individual("12345678A12")
        self.assertIsNotNone(record)
        self.assertEqual(record["first_name"], "JANE")
        self.assertEqual(
            mock_request.call_args.kwargs["params"],
            {"national_id": "12345678A12"},
        )

    @patch("apps.common.services.external_registry.requests.request")
    def test_get_company_branch_uses_lookup_company(self, mock_request):
        response = MagicMock()
        response.raise_for_status = MagicMock()
        response.json.return_value = COMPANY_PAYLOAD
        mock_request.return_value = response

        record = ExternalRegistryClient().get_company_branch("22/75")
        self.assertIsNotNone(record)
        self.assertEqual(record["company"]["registration_name"], "fincheck")
        self.assertEqual(record["external_reference"], "22/75")
        self.assertEqual(
            mock_request.call_args.kwargs["params"],
            {"search": "22/75"},
        )
