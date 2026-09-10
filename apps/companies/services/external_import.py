"""Import companies from the external registry into the local database."""

from __future__ import annotations

from django.contrib.contenttypes.models import ContentType
from django.db import transaction

from apps.common.models.models import Address, PartyDataSource
from apps.common.services.external_registry import ExternalRegistryClient
from apps.companies.models.models import Company, CompanyBranch, CompanyProfile


def _extract_current_address(payload: dict, company_data: dict) -> str | None:
    private = str(payload.get("_street_address") or "").strip()
    if private:
        return private
    primary = payload.get("primary_address")
    if isinstance(primary, dict):
        street = str(primary.get("street_address") or "").strip()
        if street:
            return street
    for source in (payload, company_data):
        value = source.get("current_address")
        if value and str(value).strip():
            return str(value).strip()
    return None


def _extract_contact(payload: dict, company_data: dict) -> tuple[str | None, str | None]:
    email = (
        company_data.get("email")
        or payload.get("email")
        or None
    )
    if email is not None:
        email = str(email).strip() or None

    mobile = (
        company_data.get("phone")
        or company_data.get("mobile_phone")
        or payload.get("phone")
        or None
    )
    if mobile is not None:
        mobile = str(mobile).strip() or None
    return email, mobile


def ensure_branch_street_address(branch: CompanyBranch, street: str | None) -> None:
    if not street or not branch:
        return
    ct = ContentType.objects.get_for_model(CompanyBranch)
    existing = Address.objects.filter(
        content_type=ct,
        object_id=branch.pk,
        address_type="physical",
        is_primary=True,
    ).first()
    if existing:
        if not (existing.street_address or "").strip():
            existing.street_address = street
            existing.save(update_fields=["street_address"])
        return
    Address.objects.create(
        content_type=ct,
        object_id=branch.pk,
        address_type="physical",
        is_primary=True,
        street_address=street,
    )


def _backfill_branch_from_lookup(
    branch: CompanyBranch | None,
    *,
    company: Company,
    street: str | None,
    email: str | None,
    mobile: str | None,
) -> CompanyBranch | None:
    if not branch:
        return None

    update_fields: list[str] = []
    if email and not (branch.email or "").strip():
        branch.email = email
        update_fields.append("email")
    if mobile and not (branch.phone or "").strip():
        branch.phone = mobile
        update_fields.append("phone")
    if update_fields:
        branch.save(update_fields=update_fields)

    if email or mobile:
        profile, _ = CompanyProfile.objects.get_or_create(company=company)
        profile_updates: list[str] = []
        if email and not (profile.email or "").strip():
            profile.email = email
            profile_updates.append("email")
        if mobile and not (profile.mobile_phone or "").strip():
            profile.mobile_phone = mobile
            profile_updates.append("mobile_phone")
        if profile_updates:
            profile.save(update_fields=profile_updates)

    ensure_branch_street_address(branch, street)
    return branch


def import_external_company(external_reference: str, *, created_by=None) -> CompanyBranch:
    """Import a company via registration name/number from lookup-company."""
    client = ExternalRegistryClient()
    payload = client.get_company_branch(external_reference)
    if not payload:
        raise ValueError("External company branch not found.")

    company_data = payload.get("company") or {}
    company_ext_ref = str(
        company_data.get("fins_number")
        or company_data.get("external_reference")
        or company_data.get("id")
        or external_reference
        or ""
    ).strip()
    street = _extract_current_address(payload, company_data)
    email, mobile = _extract_contact(payload, company_data)

    if company_ext_ref:
        existing_company = Company.objects.filter(
            external_reference=company_ext_ref, is_deleted=False
        ).first()
        if existing_company:
            hq = existing_company.branches.filter(
                is_headquarters=True, is_deleted=False
            ).first()
            if not hq:
                hq = existing_company.branches.filter(is_deleted=False).first()
            return (
                _backfill_branch_from_lookup(
                    hq,
                    company=existing_company,
                    street=street,
                    email=email,
                    mobile=mobile,
                )
                or hq
            )

    registration_number = (company_data.get("registration_number") or "").strip() or None

    if registration_number:
        by_reg = Company.objects.filter(
            registration_number=registration_number, is_deleted=False
        ).first()
        if by_reg:
            if company_ext_ref and not by_reg.external_reference:
                by_reg.external_reference = company_ext_ref
                by_reg.source = PartyDataSource.EXTERNAL
                by_reg.save(update_fields=["external_reference", "source"])
            hq = by_reg.branches.filter(is_headquarters=True, is_deleted=False).first()
            if not hq:
                hq = by_reg.branches.filter(is_deleted=False).first()
            return (
                _backfill_branch_from_lookup(
                    hq,
                    company=by_reg,
                    street=street,
                    email=email,
                    mobile=mobile,
                )
                or hq
            )

    legal_status = company_data.get("legal_status") or "private"
    valid_legal = {c[0] for c in Company.LEGAL_STATUS_CHOICES}
    if legal_status not in valid_legal:
        legal_status = "private"

    with transaction.atomic():
        company = Company(
            registration_number=registration_number,
            registration_name=company_data.get("registration_name")
            or payload.get("branch_name")
            or "Unknown Company",
            trading_name=company_data.get("trading_name"),
            legal_status=legal_status,
            industry=company_data.get("industry"),
            date_of_incorporation=company_data.get("date_of_incorporation"),
            source=PartyDataSource.EXTERNAL,
            external_reference=company_ext_ref or external_reference,
        )
        if created_by is not None:
            company.created_by = created_by
            company.updated_by = created_by
        company.save()

        if email or mobile:
            CompanyProfile.objects.create(
                company=company,
                email=email,
                mobile_phone=mobile,
            )

        company.auto_create_hq_branch()

        hq_branch = company.branches.filter(
            is_headquarters=True, is_deleted=False
        ).first()
        if hq_branch and (email or mobile):
            if email:
                hq_branch.email = email
            if mobile:
                hq_branch.phone = mobile
            hq_branch.save(update_fields=["email", "phone"])

        if hq_branch:
            ensure_branch_street_address(hq_branch, street)

    hq_branch = company.branches.filter(is_headquarters=True, is_deleted=False).first()
    if not hq_branch:
        raise ValueError("Failed to create company headquarters branch.")
    return hq_branch
