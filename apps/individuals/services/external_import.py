"""Import individuals from the external registry into the local database."""

from __future__ import annotations

from django.contrib.contenttypes.models import ContentType
from django.db import transaction

from apps.common.models.models import Address, PartyDataSource
from apps.common.services.external_registry import ExternalRegistryClient
from apps.individuals.models.models import Individual, IndividualContactDetail


def _extract_phone(payload: dict) -> str | None:
    if phone := payload.get("phone"):
        return str(phone).strip() or None
    if mobile := payload.get("mobile"):
        return str(mobile).strip() or None

    contact_details = payload.get("contact_details") or []
    for contact in contact_details:
        if not isinstance(contact, dict):
            continue
        phone_number = contact.get("phone_number")
        if phone_number:
            return str(phone_number).strip() or None
    return None


def _extract_address(payload: dict) -> str | None:
    private = str(payload.get("_street_address") or "").strip()
    if private:
        return private
    primary = payload.get("primary_address")
    if isinstance(primary, dict):
        street = str(primary.get("street_address") or "").strip()
        if street:
            return street
    value = payload.get("address")
    if value and str(value).strip():
        return str(value).strip()
    return None


def _ensure_individual_street_address(individual: Individual, street: str | None) -> None:
    if not street or not individual:
        return
    ct = ContentType.objects.get_for_model(Individual)
    existing = Address.objects.filter(
        content_type=ct,
        object_id=individual.pk,
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
        object_id=individual.pk,
        address_type="physical",
        is_primary=True,
        street_address=street,
    )


def _backfill_individual(individual: Individual, payload: dict) -> Individual:
    street = _extract_address(payload)
    phone = _extract_phone(payload)
    if phone and not individual.contact_details.filter(phone_number=phone).exists():
        has_mobile = individual.contact_details.filter(type="mobile").exists()
        if not has_mobile:
            IndividualContactDetail.objects.create(
                individual=individual,
                type="mobile",
                phone_number=phone,
            )
    _ensure_individual_street_address(individual, street)
    return individual


def import_external_individual(external_reference: str, *, created_by=None) -> Individual:
    existing = Individual.objects.filter(
        external_reference=external_reference, is_deleted=False
    ).first()
    if existing:
        client = ExternalRegistryClient()
        payload = client.get_individual(external_reference)
        if payload:
            return _backfill_individual(existing, payload)
        return existing

    client = ExternalRegistryClient()
    payload = client.get_individual(external_reference)
    if not payload:
        raise ValueError("External individual not found.")

    identification_number = (
        payload.get("identification_number")
        or payload.get("national_id")
        or ""
    )
    identification_number = str(identification_number).strip()
    if identification_number:
        by_id_number = Individual.objects.filter(
            identification_number=identification_number, is_deleted=False
        ).first()
        if by_id_number:
            if not by_id_number.external_reference:
                by_id_number.external_reference = external_reference
                by_id_number.source = PartyDataSource.EXTERNAL
                by_id_number.save(update_fields=["external_reference", "source"])
            return _backfill_individual(by_id_number, payload)

    first_name = payload.get("first_name") or payload.get("firstname") or "Unknown"
    last_name = payload.get("last_name") or payload.get("surname") or "Unknown"

    with transaction.atomic():
        individual = Individual(
            first_name=first_name,
            last_name=last_name,
            identification_type=payload.get("identification_type") or "national_id",
            identification_number=identification_number or external_reference,
            email=payload.get("email"),
            date_of_birth=payload.get("date_of_birth") or payload.get("dob"),
            gender=payload.get("gender"),
            marital_status=payload.get("marital_status"),
            source=PartyDataSource.EXTERNAL,
            external_reference=external_reference,
        )
        if created_by is not None:
            individual.created_by = created_by
            individual.updated_by = created_by
        individual.save()

        phone = _extract_phone(payload)
        if phone:
            IndividualContactDetail.objects.create(
                individual=individual,
                type="mobile",
                phone_number=phone,
            )

        _ensure_individual_street_address(individual, _extract_address(payload))

    return individual
