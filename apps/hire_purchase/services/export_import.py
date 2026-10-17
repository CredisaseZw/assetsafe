"""Import hire purchase export JSON into local models."""

from __future__ import annotations

import calendar
import hashlib
import json
import random
import re
from dataclasses import dataclass, field
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import IntegrityError, transaction
from django.utils import timezone

from apps.clients.models.models import Client
from apps.common.models import Currency
from apps.common.models.models import PartyDataSource
from apps.companies.models.models import (
    Company,
    CompanyBranch,
    CompanyProfile,
)
from apps.companies.services.external_import import ensure_branch_street_address
from apps.hire_purchase.models import HirePurchaseRegistration
from apps.individuals.models.models import Individual, IndividualContactDetail
from apps.individuals.services.external_import import _ensure_individual_street_address

EMPTY_STRINGS = {"", "none", "null", "nan", "--"}
SENTINEL_DATES = {"0001-01-01"}

# Fincheck's own fins_number. Agreements where the operator stands in as the
# financier or the debtor are not client records and are never seeded.
EXCLUDED_PARTY_IDS = {"fincheck"}

ASSET_CATEGORY_MAP = {
    "vehicles": "vehicles",
    "vehicle": "vehicles",
    "car": "vehicles",
    "motorcycle": "vehicles",
    "boat": "vehicles",
    "rv": "vehicles",
    "atv": "vehicles",
    "machinery": "machinery",
    "computers": "computers",
    "computer": "computers",
}

CONDITION_NEW = {"n", "new"}
CONDITION_USED = {"u", "used", "second hand", "second_hand", "old"}

GENDER_MAP = {
    "m": "male",
    "male": "male",
    "f": "female",
    "female": "female",
    "other": "other",
}

MARITAL_MAP = {
    "single": "single",
    "married": "married",
    "divorced": "divorced",
    "widowed": "widowed",
}


@dataclass
class ImportResult:
    currencies_created: int = 0
    currencies_updated: int = 0
    companies_created: int = 0
    companies_updated: int = 0
    individuals_created: int = 0
    individuals_updated: int = 0
    hire_purchases_created: int = 0
    hire_purchases_updated: int = 0
    hire_purchases_excluded: int = 0
    hire_purchases_start_defaulted: int = 0
    hire_purchases_end_randomized: int = 0
    skipped: list[str] = field(default_factory=list)
    excluded: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    failed_records: list[dict[str, Any]] = field(default_factory=list)

    def record_failure(self, section: str, row: dict, reason: str) -> None:
        message = f"{section}: {reason}"
        self.skipped.append(message)
        self.failed_records.append(
            {"section": section, "reason": reason, "record": row}
        )

    def record_exclusion(self, section: str, reason: str) -> None:
        """Note a row left out on purpose, as opposed to a data failure."""
        self.excluded.append(f"{section}: {reason}")
        if section == "hire_purchases":
            self.hire_purchases_excluded += 1


def _blank(value: Any) -> bool:
    if value is None:
        return True
    text = str(value).strip()
    return not text or text.lower() in EMPTY_STRINGS


def _clean_str(value: Any, *, default: str = "") -> str:
    if _blank(value):
        return default
    return str(value).strip()


def _parse_date(value: Any) -> date | None:
    if _blank(value):
        return None
    text = str(value).strip()
    if text in SENTINEL_DATES or text.lower() in EMPTY_STRINGS:
        return None
    if "T" in text:
        text = text.split("T", 1)[0]
    try:
        return date.fromisoformat(text)
    except ValueError:
        for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
            try:
                return datetime.strptime(text, fmt).date()
            except ValueError:
                continue
    return None


def _add_months(value: date, months: int) -> date:
    """Return ``value`` shifted forward by whole ``months``, clamping the day."""
    month_index = value.month - 1 + months
    year = value.year + month_index // 12
    month = month_index % 12 + 1
    day = min(value.day, calendar.monthrange(year, month)[1])
    return date(year, month, day)


def _random_end_date(start: date, agreement_number: str) -> date:
    """
    Pick a plausible agreement term (12-60 months) for a row with no due date.

    The generator is seeded from the agreement number so re-importing the same
    export keeps the end date it assigned before instead of churning it.
    """
    seed = int.from_bytes(
        hashlib.sha256(agreement_number.encode("utf-8")).digest()[:8], "big"
    )
    months = random.Random(seed).randint(12, 60)
    return _add_months(start, months)


def _parse_decimal(value: Any, *, default: Decimal | None = None) -> Decimal | None:
    if _blank(value):
        return default
    text = str(value).strip().replace(",", "")
    try:
        return Decimal(text)
    except (InvalidOperation, ValueError):
        return default


def _parse_year(value: Any) -> int | None:
    if _blank(value):
        return None
    try:
        year = int(float(str(value).strip()))
    except (TypeError, ValueError):
        return None
    if 1900 <= year <= 2100:
        return year
    return None


def _parse_instalment_day(value: Any) -> int:
    if _blank(value):
        return 1
    try:
        day = int(float(str(value).strip()))
    except (TypeError, ValueError):
        return 1
    if 1 <= day <= 31:
        return day
    return 1


def _map_asset_category(asset_type: Any) -> tuple[str, str]:
    raw = _clean_str(asset_type)
    key = raw.lower()
    category = ASSET_CATEGORY_MAP.get(key, "equipment")
    return category, raw


def _map_condition(value: Any) -> str:
    raw = _clean_str(value)
    if not raw:
        return ""
    key = raw.lower()
    if key in CONDITION_NEW:
        return "new"
    if key in CONDITION_USED:
        return "second_hand"
    return raw[:20]


def _map_gender(value: Any) -> str | None:
    raw = _clean_str(value).lower()
    if not raw:
        return None
    return GENDER_MAP.get(raw)


def _map_marital_status(value: Any) -> str | None:
    raw = _clean_str(value).lower()
    if not raw:
        return None
    return MARITAL_MAP.get(raw)


def _safe_email(value: Any) -> str | None:
    email = _clean_str(value)
    if not email:
        return None

    email = re.sub(r"^email:\s*", "", email, flags=re.IGNORECASE)
    for candidate in re.split(r"[,/;]", email):
        candidate = candidate.strip()
        if not candidate:
            continue
        try:
            validate_email(candidate)
        except ValidationError:
            continue
        return candidate
    return None


def _phone_numbers(value: Any) -> list[str]:
    """Split source values that contain multiple phone numbers."""
    raw = _clean_str(value)
    if not raw:
        return []
    return list(
        dict.fromkeys(part.strip() for part in re.split(r"[,/;]", raw) if part.strip())
    )


def _hq_branch(company: Company) -> CompanyBranch | None:
    return (
        company.branches.filter(is_headquarters=True, is_deleted=False).first()
        or company.branches.filter(is_deleted=False).first()
    )


def import_currencies(
    rows: list[dict], result: ImportResult
) -> dict[str, Currency | None]:
    by_code: dict[str, Currency | None] = {}
    for row in rows:
        code = _clean_str(row.get("code")).upper()
        if not code or code == "NOT GIVEN" or len(code) > 3:
            by_code[code or "NOT GIVEN"] = None
            continue
        name = _clean_str(row.get("name_of_currency")) or code
        symbol = code
        obj, created = Currency.objects.update_or_create(
            code=code,
            defaults={"name": name, "symbol": symbol},
        )
        by_code[code] = obj
        if created:
            result.currencies_created += 1
        else:
            result.currencies_updated += 1
    return by_code


def import_company(row: dict, result: ImportResult) -> CompanyBranch | None:
    fins = _clean_str(row.get("fins_number"))
    if not fins:
        result.record_failure("companies", row, "missing fins_number")
        return None

    registration_name = _clean_str(row.get("registration_name")) or fins
    registration_number = _clean_str(row.get("registration_number")) or None
    if registration_number == "0":
        # Ambiguous placeholder used by multiple source rows.
        registration_number = None
    trading_name = _clean_str(row.get("trading_name")) or None
    industry = _clean_str(row.get("industry")) or None
    if industry and industry.lower() in EMPTY_STRINGS:
        industry = None
    date_of_incorporation = _parse_date(row.get("registration_date"))
    email = _safe_email(row.get("email"))
    phone_numbers = _phone_numbers(row.get("mobile_phone"))
    primary_mobile = phone_numbers[0] if phone_numbers else None
    street = _clean_str(row.get("current_address")) or None
    vat_number = _clean_str(row.get("vat_number")) or None
    website = _clean_str(row.get("website")) or None
    if website and not re.match(r"^https?://", website, re.I):
        website = f"https://{website}"

    company = Company.objects.filter(external_reference=fins, is_deleted=False).first()
    created = False
    if not company:
        company = Company(
            registration_name=registration_name,
            source=PartyDataSource.EXTERNAL,
            external_reference=fins,
        )
        created = True

    company.registration_name = registration_name
    company.trading_name = trading_name
    company.registration_number = registration_number
    company.industry = industry
    company.date_of_incorporation = date_of_incorporation
    company.source = PartyDataSource.EXTERNAL
    company.external_reference = fins
    company.is_deleted = False
    company.is_active = True
    company.save()

    profile, _ = CompanyProfile.objects.get_or_create(company=company)
    profile_updates: list[str] = []
    if email and profile.email != email:
        profile.email = email
        profile_updates.append("email")
    if primary_mobile and profile.mobile_phone != primary_mobile:
        profile.mobile_phone = primary_mobile
        profile_updates.append("mobile_phone")
    if vat_number and profile.vat_number != vat_number:
        profile.vat_number = vat_number
        profile_updates.append("vat_number")
    if website:
        profile.website = website
        profile_updates.append("website")
    if date_of_incorporation and profile.registration_date != date_of_incorporation:
        profile.registration_date = date_of_incorporation
        profile_updates.append("registration_date")
    if profile_updates:
        fields = list(dict.fromkeys(profile_updates))
        try:
            profile.save(update_fields=fields)
        except Exception:
            # Drop invalid website and retry remaining profile fields.
            profile.website = None
            remaining = [f for f in fields if f != "website"]
            if remaining:
                profile.save(update_fields=remaining)

    branch = _hq_branch(company)
    if not branch:
        branch = company.auto_create_hq_branch()
    if not branch:
        result.record_failure(
            "companies", row, f"{fins}: failed to create HQ branch"
        )
        return None

    branch_updates: list[str] = []
    if email and branch.email != email:
        branch.email = email
        branch_updates.append("email")
    if primary_mobile and branch.phone != primary_mobile:
        branch.phone = primary_mobile
        branch_updates.append("phone")
    if branch_updates:
        branch.save(update_fields=branch_updates)

    ensure_branch_street_address(branch, street)

    if created:
        result.companies_created += 1
    else:
        result.companies_updated += 1
    return branch


def import_companies(
    rows: list[dict], result: ImportResult, *, stdout=None, progress_every: int = 100
) -> dict[str, CompanyBranch]:
    by_fins: dict[str, CompanyBranch] = {}
    for index, row in enumerate(rows, start=1):
        try:
            with transaction.atomic():
                branch = import_company(row, result)
        except Exception as exc:  # noqa: BLE001 - isolate a bad source row
            result.record_failure("companies", row, f"row {index}: {exc}")
            if stdout and progress_every and index % progress_every == 0:
                stdout.write(f"Companies: {index}/{len(rows)}")
            continue
        if branch is None:
            if not any(item.get("record") is row for item in result.failed_records):
                result.record_failure(
                    "companies", row, f"row {index}: skipped (no reason recorded)"
                )
            if stdout and progress_every and index % progress_every == 0:
                stdout.write(f"Companies: {index}/{len(rows)}")
            continue
        fins = _clean_str(row.get("fins_number"))
        if fins:
            by_fins[fins] = branch
        if stdout and progress_every and index % progress_every == 0:
            stdout.write(f"Companies: {index}/{len(rows)}")
    return by_fins


def import_individual(row: dict, result: ImportResult) -> Individual | None:
    fins = _clean_str(row.get("fins_number"))
    national_id = _clean_str(row.get("national_id"))
    if not fins and not national_id:
        result.record_failure(
            "individuals", row, "missing fins_number and national_id"
        )
        return None

    first_name = _clean_str(row.get("firstname")) or "Unknown"
    last_name = _clean_str(row.get("surname")) or "Unknown"
    dob = _parse_date(row.get("dob"))
    gender = _map_gender(row.get("gender"))
    marital_status = _map_marital_status(row.get("marital_status"))
    street = _clean_str(row.get("address")) or None
    phone = _clean_str(row.get("mobile") or row.get("telephone_no")) or None
    id_type_raw = _clean_str(row.get("identification_type")).lower().replace(" ", "_")
    valid_id_types = {c[0] for c in Individual.IDENTIFICATION_TYPES}
    identification_type = (
        id_type_raw if id_type_raw in valid_id_types else "national_id"
    )
    identification_number = national_id or fins

    individual = None
    if fins:
        individual = Individual.objects.filter(
            external_reference=fins, is_deleted=False
        ).first()
    if individual is None and identification_number:
        individual = Individual.objects.filter(
            identification_number=identification_number, is_deleted=False
        ).first()

    created = individual is None
    if created:
        individual = Individual(
            first_name=first_name,
            last_name=last_name,
            identification_type=identification_type,
            identification_number=identification_number,
            source=PartyDataSource.EXTERNAL,
            external_reference=fins or None,
        )
    else:
        individual.first_name = first_name
        individual.last_name = last_name
        individual.identification_type = identification_type
        if identification_number:
            individual.identification_number = identification_number
        individual.source = PartyDataSource.EXTERNAL
        if fins:
            individual.external_reference = fins
        individual.is_deleted = False
        individual.is_active = True

    individual.date_of_birth = dob
    individual.gender = gender
    individual.marital_status = marital_status
    individual.save()

    if phone and not individual.contact_details.filter(phone_number=phone).exists():
        IndividualContactDetail.objects.create(
            individual=individual,
            type="mobile",
            phone_number=phone,
        )
    _ensure_individual_street_address(individual, street)

    if created:
        result.individuals_created += 1
    else:
        result.individuals_updated += 1
    return individual


def import_individuals(
    rows: list[dict], result: ImportResult, *, stdout=None, progress_every: int = 100
) -> dict[str, Individual]:
    by_fins: dict[str, Individual] = {}
    for index, row in enumerate(rows, start=1):
        try:
            with transaction.atomic():
                individual = import_individual(row, result)
        except Exception as exc:  # noqa: BLE001 - isolate a bad source row
            result.record_failure("individuals", row, f"row {index}: {exc}")
            if stdout and progress_every and index % progress_every == 0:
                stdout.write(f"Individuals: {index}/{len(rows)}")
            continue
        if individual is None:
            if not any(item.get("record") is row for item in result.failed_records):
                result.record_failure(
                    "individuals", row, f"row {index}: skipped (no reason recorded)"
                )
            if stdout and progress_every and index % progress_every == 0:
                stdout.write(f"Individuals: {index}/{len(rows)}")
            continue
        fins = _clean_str(row.get("fins_number"))
        if fins:
            by_fins[fins] = individual
        if stdout and progress_every and index % progress_every == 0:
            stdout.write(f"Individuals: {index}/{len(rows)}")
    return by_fins


def _ensure_financier_client(
    branch: CompanyBranch, cache: dict[int, Client] | None = None
) -> Client:
    if cache is not None and branch.pk in cache:
        return cache[branch.pk]
    ct = ContentType.objects.get_for_model(CompanyBranch)
    client = Client.objects.filter(
        client_content_type=ct, client_object_id=branch.pk
    ).first()
    if client is None:
        client = Client.objects.create(
            client_content_type=ct,
            client_object_id=branch.pk,
            client_type="CLIENT",
            status="ACTIVE",
        )
    if cache is not None:
        cache[branch.pk] = client
    return client


def _agreement_number(row: dict, used_this_run: set[str]) -> str:
    """
    Prefer agreement_number, then agreement, then HP-{id}.

    Within a single import pass, duplicate bases become ``{base}#{id}``.
    Existing DB rows with the same base are updated on later runs (the used
    set only tracks this pass, so the base remains available for lookup).
    """
    export_id = row.get("id")
    base = (
        _clean_str(row.get("agreement_number"))
        or _clean_str(row.get("agreement"))
        or f"HP-{export_id}"
    )
    if base not in used_this_run:
        used_this_run.add(base)
        return base
    candidate = f"{base}#{export_id}"
    used_this_run.add(candidate)
    return candidate


def _serial_number(row: dict) -> str:
    for key in ("serial", "serial_number"):
        value = _clean_str(row.get(key))
        if value:
            return value
    return ""


def _mv_registration(row: dict) -> str:
    for key in ("reg_number", "asset_reg_number"):
        value = _clean_str(row.get(key))
        if value:
            return value
    return ""


def _hp_label(row: dict) -> str:
    """Identify one hire purchase row in skip and failure messages."""
    return f"HP id={row.get('id')}"


def _identity_conflict(
    *,
    financier: Client,
    purchaser_company: CompanyBranch | None,
    purchaser_individual: Individual | None,
    make: str,
    mv_registration_number: str,
    serial_number: str,
) -> HirePurchaseRegistration | None:
    filters = {
        "financier": financier,
        "make": make,
        "purchaser_company": purchaser_company,
        "purchaser_individual": purchaser_individual,
    }
    candidates = HirePurchaseRegistration.objects.filter(**filters)
    if mv_registration_number:
        conflict = candidates.filter(
            mv_registration_number=mv_registration_number
        ).first()
        if conflict is not None:
            return conflict
    if serial_number:
        conflict = candidates.filter(serial_number=serial_number).first()
        if conflict is not None:
            return conflict
    if not mv_registration_number and not serial_number:
        return candidates.filter(mv_registration_number="", serial_number="").first()
    return None


def import_hire_purchase(
    row: dict,
    *,
    companies: dict[str, CompanyBranch],
    individuals: dict[str, Individual],
    currencies: dict[str, Currency | None],
    used_agreements: set[str],
    result: ImportResult,
    financier_cache: dict[int, Client] | None = None,
    existing_hire_purchases: dict[str, HirePurchaseRegistration] | None = None,
    currency_cache: dict[str, Currency | None] | None = None,
) -> HirePurchaseRegistration | None:
    label = _hp_label(row)

    debtor_company_id = _clean_str(row.get("debtor_company")) or None
    debtor_individual_id = _clean_str(row.get("debtor_individual")) or None
    financier_company_id = _clean_str(row.get("financier_company")) or None

    if (debtor_company_id or "").lower() in EXCLUDED_PARTY_IDS or (
        debtor_individual_id or ""
    ).lower() in EXCLUDED_PARTY_IDS:
        result.record_exclusion(
            "hire_purchases", f"{label}: excluded (debtor is fincheck)"
        )
        return None
    if (financier_company_id or "").lower() in EXCLUDED_PARTY_IDS:
        result.record_exclusion(
            "hire_purchases", f"{label}: excluded (financier is fincheck)"
        )
        return None

    purchaser_company = None
    purchaser_individual = None
    if debtor_company_id:
        purchaser_company = companies.get(debtor_company_id)
        if purchaser_company is None:
            result.record_failure(
                "hire_purchases",
                row,
                f"{label}: unknown debtor_company {debtor_company_id}",
            )
            return None
    elif debtor_individual_id:
        purchaser_individual = individuals.get(debtor_individual_id)
        if purchaser_individual is None:
            result.record_failure(
                "hire_purchases",
                row,
                f"{label}: unknown debtor_individual {debtor_individual_id}",
            )
            return None
    else:
        result.record_failure("hire_purchases", row, f"{label}: no debtor")
        return None

    if not financier_company_id:
        result.record_failure("hire_purchases", row, f"{label}: no financier")
        return None
    financier_branch = companies.get(financier_company_id)
    if financier_branch is None:
        result.record_failure(
            "hire_purchases",
            row,
            f"{label}: unknown financier_company {financier_company_id}",
        )
        return None
    financier = _ensure_financier_client(financier_branch, financier_cache)

    agreement_number = _agreement_number(row, used_agreements)
    start = _parse_date(row.get("agreement_start_date"))
    end = _parse_date(row.get("agreement_due_date"))
    data_date = _parse_date(row.get("data_date")) or _parse_date(
        row.get("date_created")
    )
    start_defaulted = False
    if start is None:
        start = data_date or timezone.now().date()
        start_defaulted = True
    end_randomized = False
    if end is None:
        end = _random_end_date(start, agreement_number)
        end_randomized = True

    currency_code = _clean_str(row.get("currency")).upper()
    currency = None
    if currency_code and currency_code != "NOT GIVEN":
        currency = (
            currency_cache.get(currency_code)
            if currency_cache is not None
            else currencies.get(currency_code)
        )
        if currency is None:
            if currency_cache is None or currency_code not in currency_cache:
                currency = Currency.objects.filter(code=currency_code).first()
                if currency_cache is not None:
                    currency_cache[currency_code] = currency

    asset_category, asset_type = _map_asset_category(row.get("asset_type"))
    purchase_amount = _parse_decimal(row.get("purchase_amount"), default=Decimal("0"))
    instalment_amount = _parse_decimal(
        row.get("installment_amount"), default=Decimal("0")
    )
    total_paid = _parse_decimal(row.get("total_paid_to_date"), default=Decimal("0"))
    make = _clean_str(row.get("make"))
    model = _clean_str(row.get("model"))
    if model.lower() == "nan":
        model = ""
    mv_registration_number = _mv_registration(row)
    serial_number = _serial_number(row)

    existing = (
        existing_hire_purchases.get(agreement_number)
        if existing_hire_purchases is not None
        else HirePurchaseRegistration.objects.filter(
            agreement_number=agreement_number
        ).first()
    )
    if existing is None:
        conflict = _identity_conflict(
            financier=financier,
            purchaser_company=purchaser_company,
            purchaser_individual=purchaser_individual,
            make=make,
            mv_registration_number=mv_registration_number,
            serial_number=serial_number,
        )
        if conflict is not None:
            result.record_failure(
                "hire_purchases",
                row,
                f"{label}: duplicate asset identity; existing HP id={conflict.pk}",
            )
            return None
    created = existing is None
    hp = existing or HirePurchaseRegistration(agreement_number=agreement_number)

    hp.agreement_number = agreement_number
    hp.financier = financier
    hp.purchaser_company = purchaser_company
    hp.purchaser_individual = purchaser_individual
    hp.purchaser_type = "company" if purchaser_company else "individual"
    hp.asset_category = asset_category
    hp.asset_type = asset_type
    hp.make = make
    hp.model = model
    hp.year_of_make = _parse_year(row.get("year"))
    hp.condition = _map_condition(row.get("condition"))
    hp.mv_registration_number = mv_registration_number
    hp.chassis_number = _clean_str(row.get("chasis"))
    hp.engine_number = _clean_str(row.get("engine_number"))
    hp.serial_number = serial_number
    hp.currency = currency
    hp.purchase_amount = purchase_amount or Decimal("0")
    hp.instalment_amount = instalment_amount or Decimal("0")
    hp.instalment_day = _parse_instalment_day(row.get("installment_date"))
    hp.total_paid_to_date = total_paid or Decimal("0")
    hp.agreement_start_date = start
    hp.agreement_end_date = end
    hp.data_date = data_date or start
    hp.data_source_name = _clean_str(row.get("data_source"))
    hp.closure_confirmed = bool(row.get("is_closed"))

    try:
        with transaction.atomic():
            hp.save()
    except IntegrityError as exc:
        reason = f"{label}: integrity error ({exc})"
        result.errors.append(reason)
        result.record_failure("hire_purchases", row, reason)
        return None
    except Exception as exc:  # noqa: BLE001 - continue importing remaining rows
        reason = f"{label}: {exc}"
        result.errors.append(reason)
        result.record_failure("hire_purchases", row, reason)
        return None

    if created:
        result.hire_purchases_created += 1
    else:
        result.hire_purchases_updated += 1
    if start_defaulted:
        result.hire_purchases_start_defaulted += 1
    if end_randomized:
        result.hire_purchases_end_randomized += 1
    return hp


def import_hire_purchases(
    rows: list[dict],
    *,
    companies: dict[str, CompanyBranch],
    individuals: dict[str, Individual],
    currencies: dict[str, Currency | None],
    result: ImportResult,
    stdout=None,
    progress_every: int = 100,
) -> None:
    used_agreements: set[str] = set()
    financier_cache: dict[int, Client] = {}
    currency_cache = dict(currencies)
    agreement_names: list[str] = []
    agreement_seen: set[str] = set()
    for row in rows:
        agreement_name = _agreement_number(row, agreement_seen)
        agreement_names.append(agreement_name)
    existing_hire_purchases = {
        item.agreement_number: item
        for item in HirePurchaseRegistration.objects.filter(
            agreement_number__in=agreement_names
        )
    }
    used_agreements.clear()
    for index, row in enumerate(rows, start=1):
        exclusions_before = len(result.excluded)
        try:
            with transaction.atomic():
                hp = import_hire_purchase(
                    row,
                    companies=companies,
                    individuals=individuals,
                    currencies=currencies,
                    used_agreements=used_agreements,
                    result=result,
                    financier_cache=financier_cache,
                    existing_hire_purchases=existing_hire_purchases,
                    currency_cache=currency_cache,
                )
        except Exception as exc:  # noqa: BLE001 - isolate a bad source row
            result.record_failure(
                "hire_purchases", row, f"{_hp_label(row)}: row {index}: {exc}"
            )
            if stdout and progress_every and index % progress_every == 0:
                stdout.write(f"Hire purchases: {index}/{len(rows)}")
            continue
        if (
            hp is None
            and len(result.excluded) == exclusions_before
            and not any(item.get("record") is row for item in result.failed_records)
        ):
            result.record_failure(
                "hire_purchases",
                row,
                f"{_hp_label(row)}: row {index}: skipped (no reason recorded)",
            )
        if stdout and progress_every and index % progress_every == 0:
            stdout.write(f"Hire purchases: {index}/{len(rows)}")


def write_failed_export(path: str | Path, result: ImportResult) -> None:
    failed_path = Path(path)
    with failed_path.open("w", encoding="utf-8") as handle:
        json.dump(
            {
                "format": "hire_purchase_import_failures",
                "version": 1,
                "failed_records": result.failed_records,
            },
            handle,
            ensure_ascii=False,
            indent=2,
        )


def load_export(path: str | Path) -> dict:
    with open(path, encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError("Export file must be a JSON object.")
    return data


def import_hire_purchase_export(
    path: str | Path, *, stdout=None, progress_every: int = 100
) -> ImportResult:
    """
    Import currencies, companies, individuals, then hire purchases from an
    export JSON file, linking hire purchases via fins_number IDs.
    """
    data = load_export(path)
    result = ImportResult()

    currency_rows = data.get("currencies") or []
    currencies = {}
    for index, row in enumerate(currency_rows, start=1):
        try:
            with transaction.atomic():
                currencies.update(import_currencies([row], result))
        except Exception as exc:  # noqa: BLE001 - isolate a bad source row
            result.record_failure("currencies", row, f"row {index}: {exc}")
        if stdout and progress_every and index % progress_every == 0:
            stdout.write(f"Currencies: {index}/{len(currency_rows)}")
    if stdout:
        stdout.write(
            f"Currencies: created={result.currencies_created} "
            f"updated={result.currencies_updated}"
        )

    company_rows = data.get("companies") or []
    companies = import_companies(
        company_rows, result, stdout=stdout, progress_every=progress_every
    )
    if stdout:
        stdout.write(
            f"Companies: created={result.companies_created} "
            f"updated={result.companies_updated}"
        )

    individual_rows = data.get("individuals") or []
    individuals = import_individuals(
        individual_rows, result, stdout=stdout, progress_every=progress_every
    )
    if stdout:
        stdout.write(
            f"Individuals: created={result.individuals_created} "
            f"updated={result.individuals_updated}"
        )

    import_hire_purchases(
        data.get("hire_purchases") or [],
        companies=companies,
        individuals=individuals,
        currencies=currencies,
        result=result,
        stdout=stdout,
        progress_every=progress_every,
    )
    if stdout:
        stdout.write(
            f"Hire purchases: created={result.hire_purchases_created} "
            f"updated={result.hire_purchases_updated} "
            f"excluded={result.hire_purchases_excluded} "
            f"start_defaulted={result.hire_purchases_start_defaulted} "
            f"end_randomized={result.hire_purchases_end_randomized}"
        )
        if result.excluded:
            stdout.write(f"Excluded {len(result.excluded)} row(s):")
            for item in result.excluded:
                stdout.write(f"  - {item}")
        if result.skipped:
            stdout.write(f"Skipped {len(result.skipped)} hire purchase row(s):")
            for item in result.skipped:
                stdout.write(f"  - {item}")
        if result.errors:
            stdout.write(f"Errors ({len(result.errors)}):")
            for item in result.errors:
                stdout.write(f"  - {item}")

    return result
