"""Client for searching and fetching party records from an external lookup API."""

from __future__ import annotations

import logging
import re
from typing import Any

import requests
from django.conf import settings

logger = logging.getLogger(__name__)

# Zimbabwe national ID after normalize:
# 2-digit register + 6–7 digit serial + check letter + 2-digit district (11 or 12 chars).
# Accepted input forms include 12345678A12, 082047823Q29, 12-345678-A-12, 08-2047823-Q-29.
NATIONAL_ID_PATTERN = re.compile(r"^\d{2}\d{6,7}[A-Z]\d{2}$")


def normalize_national_id(query: str) -> str:
    """Strip separators/spaces and uppercase for national-id comparison and lookup."""
    return re.sub(r"[^0-9A-Za-z]", "", (query or "").strip()).upper()


def looks_like_national_id(query: str) -> bool:
    """Return True when query is a Zimbabwe national-id-like token (not a name search)."""
    return bool(NATIONAL_ID_PATTERN.match(normalize_national_id(query)))


def primary_address_from_street(street: str | None) -> dict[str, Any] | None:
    """Map free-text address into the same shape AddressSerializer returns."""
    text = str(street or "").strip()
    if not text:
        return None
    return {
        "id": None,
        "address_type": "physical",
        "is_primary": True,
        "street_address": text,
        "line_2": None,
        "postal_code": None,
        "latitude": None,
        "longitude": None,
        "country": None,
        "province": None,
        "city": None,
        "suburb": None,
        "date_created": None,
        "date_updated": None,
    }


def _street_from_branch_payload(row: dict[str, Any]) -> str | None:
    private = str(row.get("_street_address") or "").strip()
    if private:
        return private
    primary = row.get("primary_address")
    if isinstance(primary, dict):
        street = str(primary.get("street_address") or "").strip()
        if street:
            return street
    company = row.get("company") if isinstance(row.get("company"), dict) else {}
    for value in (row.get("current_address"), company.get("current_address")):
        if value and str(value).strip():
            return str(value).strip()
    return None


def _apply_compatible_address_to_local(
    local: dict[str, Any], external: dict[str, Any]
) -> None:
    """Persist street onto a local HQ branch when search matched an external hit.

    Search payloads stay slim (no primary_address); only DB backfill runs here.
    """
    street = _street_from_branch_payload(external)
    if not street:
        return

    branch_id = local.get("id")
    if not branch_id:
        return

    from apps.companies.models.models import CompanyBranch
    from apps.companies.services.external_import import ensure_branch_street_address

    branch = CompanyBranch.objects.filter(pk=branch_id).first()
    if not branch:
        return
    ensure_branch_street_address(branch, street)


def merge_individual_search_results(
    local_results: list[dict[str, Any]],
    external_results: list[dict[str, Any]],
    *,
    limit: int = 25,
) -> list[dict[str, Any]]:
    """Local hits first, then external rows not already covered by ID or external_reference."""
    merged: list[dict[str, Any]] = list(local_results)[:limit]
    seen_ids: set[str] = set()
    seen_refs: set[str] = set()

    for row in merged:
        id_num = normalize_national_id(str(row.get("identification_number") or ""))
        if id_num:
            seen_ids.add(id_num)
        ref = str(row.get("external_reference") or "").strip()
        if ref:
            seen_refs.add(ref)
            normalized_ref = normalize_national_id(ref)
            if normalized_ref:
                seen_refs.add(normalized_ref)
                seen_ids.add(normalized_ref)

    for row in external_results:
        if len(merged) >= limit:
            break
        id_num = normalize_national_id(str(row.get("identification_number") or ""))
        ref = str(row.get("external_reference") or "").strip()
        if id_num and id_num in seen_ids:
            continue
        if ref and (ref in seen_refs or normalize_national_id(ref) in seen_refs):
            continue
        if id_num and id_num in seen_refs:
            continue
        merged.append(row)
        if id_num:
            seen_ids.add(id_num)
        if ref:
            seen_refs.add(ref)
            normalized_ref = normalize_national_id(ref)
            if normalized_ref:
                seen_refs.add(normalized_ref)

    return merged


def merge_company_search_results(
    local_results: list[dict[str, Any]],
    external_results: list[dict[str, Any]],
    *,
    limit: int = 25,
) -> list[dict[str, Any]]:
    """Local hits first, then external rows not already covered by reg no or external ref.

    When an external hit matches a local row that is missing primary_address, copy the
    already-normalized address onto that local row so the response stays compatible.
    """
    merged: list[dict[str, Any]] = [dict(row) for row in local_results[:limit]]
    seen_regs: set[str] = set()
    seen_refs: set[str] = set()

    def _ingest(row: dict[str, Any]) -> None:
        company = row.get("company") if isinstance(row.get("company"), dict) else {}
        reg = str(company.get("registration_number") or "").strip().lower()
        if reg:
            seen_regs.add(reg)
        for key in (
            row.get("external_reference"),
            company.get("external_reference"),
            company.get("fins_number"),
        ):
            ref = str(key or "").strip().lower()
            if ref:
                seen_refs.add(ref)

    for row in merged:
        _ingest(row)

    for row in external_results:
        company = row.get("company") if isinstance(row.get("company"), dict) else {}
        reg = str(company.get("registration_number") or "").strip().lower()
        refs = {
            str(v or "").strip().lower()
            for v in (
                row.get("external_reference"),
                company.get("external_reference"),
                company.get("fins_number"),
            )
            if v
        }
        if (reg and reg in seen_regs) or (refs & seen_refs):
            for local in merged:
                local_company = (
                    local.get("company")
                    if isinstance(local.get("company"), dict)
                    else {}
                )
                local_reg = str(
                    local_company.get("registration_number") or ""
                ).strip().lower()
                local_refs = {
                    str(v or "").strip().lower()
                    for v in (
                        local.get("external_reference"),
                        local_company.get("external_reference"),
                        local_company.get("fins_number"),
                    )
                    if v
                }
                if (reg and local_reg == reg) or (refs & local_refs):
                    _apply_compatible_address_to_local(local, row)
            continue
        if len(merged) >= limit:
            break
        merged.append(dict(row))
        _ingest(row)

    return merged


class ExternalRegistryClient:
    """HTTP client for external lookup-person / lookup-company endpoints."""

    def __init__(self) -> None:
        self.base_url = (
            getattr(settings, "EXTERNAL_REGISTRY_BASE_URL", "") or ""
        ).rstrip("/")
        self.username = getattr(settings, "EXTERNAL_REGISTRY_USERNAME", "") or ""
        self.token = getattr(settings, "EXTERNAL_REGISTRY_TOKEN", "") or ""
        self.timeout = getattr(settings, "EXTERNAL_REGISTRY_TIMEOUT", 10)

    @property
    def is_configured(self) -> bool:
        return bool(self.base_url and self.username and self.token)

    def _headers(self) -> dict[str, str]:
        return {
            "Accept": "application/json",
            "Username": self.username,
            "Token": self.token,
        }

    def _request(self, method: str, path: str, **kwargs) -> Any | None:
        if not self.is_configured:
            return None

        url = f"{self.base_url}{path}"
        try:
            response = requests.request(
                method,
                url,
                headers=self._headers(),
                timeout=self.timeout,
                **kwargs,
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as exc:
            logger.warning(
                "External registry request failed (%s %s): %s", method, url, exc
            )
            return None

    @staticmethod
    def _map_individual(remote: dict[str, Any]) -> dict[str, Any]:
        """Normalize lookup-person into slim SearchOption-compatible fields."""
        national_id = str(remote.get("national_id") or "").strip()
        address_text = remote.get("address")
        if address_text is not None:
            address_text = str(address_text).strip() or None
        phone = remote.get("mobile")
        phone = str(phone).strip() if phone not in (None, "") else None
        email = remote.get("email")
        email = str(email).strip() if email not in (None, "") else None
        return {
            "id": None,
            "first_name": remote.get("firstname") or "",
            "last_name": remote.get("surname") or "",
            "identification_number": national_id,
            "phone": phone,
            "email": email,
            "source": "external",
            "external_reference": national_id,
            # Import-only; stripped from public search contract.
            "_street_address": address_text,
        }

    @staticmethod
    def _map_company_branch(remote: dict[str, Any]) -> dict[str, Any]:
        """Normalize lookup-company into slim SearchOption-compatible fields."""
        fins_number = str(remote.get("fins_number") or "").strip()
        registration_number = str(remote.get("registration_number") or "").strip()
        registration_name = str(remote.get("registration_name") or "").strip()
        trading_name = remote.get("trading_name")
        if trading_name is not None:
            trading_name = str(trading_name).strip() or None

        # lookup-company/?search= expects reg name/number — not fins_number.
        searchable_ref = registration_number or registration_name or fins_number
        identity_ref = fins_number or searchable_ref
        display_name = registration_name or "Unknown Company"

        street = remote.get("current_address")
        street = str(street).strip() if street not in (None, "") else None

        email = remote.get("email")
        email = str(email).strip() if email not in (None, "") else None
        phone = remote.get("mobile_phone")
        phone = str(phone).strip() if phone not in (None, "") else None

        company = {
            "registration_number": registration_number or None,
            "registration_name": display_name,
            "trading_name": trading_name,
            "external_reference": identity_ref,
        }
        return {
            "id": None,
            "branch_name": display_name,
            "is_headquarters": True,
            "company": company,
            "email": email,
            "phone": phone,
            "external_reference": searchable_ref,
            "source": "external",
            # Import-only; stripped from public search contract.
            "_street_address": street,
        }

    def search_individuals(self, query: str) -> list[dict[str, Any]]:
        if not looks_like_national_id(query):
            return []

        national_id = normalize_national_id(query)
        payload = self._request(
            "GET",
            "/lookup-person/",
            params={"national_id": national_id},
        )
        if not isinstance(payload, dict) or not payload.get("found"):
            return []
        individual = payload.get("individual")
        if not isinstance(individual, dict):
            return []
        return [self._map_individual(individual)]

    def search_companies(self, query: str) -> list[dict[str, Any]]:
        payload = self._request(
            "GET",
            "/lookup-company/",
            params={"search": query.strip()},
        )
        if not isinstance(payload, dict) or not payload.get("found"):
            return []
        company = payload.get("company")
        if not isinstance(company, dict):
            return []
        return [self._map_company_branch(company)]

    def get_individual(self, external_reference: str) -> dict[str, Any] | None:
        payload = self._request(
            "GET",
            "/lookup-person/",
            params={"national_id": external_reference},
        )
        if not isinstance(payload, dict) or not payload.get("found"):
            return None
        individual = payload.get("individual")
        if not isinstance(individual, dict):
            return None
        return self._map_individual(individual)

    def get_company_branch(self, external_reference: str) -> dict[str, Any] | None:
        """Re-fetch via lookup-company using reg number/name (or other searchable ref)."""
        ref = (external_reference or "").strip()
        if not ref:
            return None

        # Try the given ref, then common variants (fins refs are not searchable).
        candidates = [ref]
        if ref.upper().startswith("FNC-"):
            # Fins numbers are not valid ?search= values; caller should pass reg name/number.
            logger.warning(
                "lookup-company called with fins-style ref %r; search may fail",
                ref,
            )

        for candidate in candidates:
            payload = self._request(
                "GET",
                "/lookup-company/",
                params={"search": candidate},
            )
            if not isinstance(payload, dict) or not payload.get("found"):
                continue
            company = payload.get("company")
            if isinstance(company, dict):
                return self._map_company_branch(company)
        return None

    def get_company(self, external_reference: str) -> dict[str, Any] | None:
        """Alias kept for import services — external_reference is fins/registration id."""
        return self.get_company_branch(external_reference)
