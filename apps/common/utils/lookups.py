"""Helpers for DB-backed PartyType / BaseAssetType / AssetCondition lookups."""

from __future__ import annotations

from django.core.exceptions import ValidationError as DjangoValidationError

from apps.common.models import LookupOption


def list_lookup_choices(category: str) -> list[dict[str, str]]:
    """Return ``[{value, label}, ...]`` for active options in a category."""
    return [
        {"value": row.value, "label": row.label}
        for row in LookupOption.objects.filter(
            category=category, is_active=True
        ).order_by("sort_order", "label")
    ]


def ensure_valid_lookup_value(category: str, value: str | None, *, field: str) -> str:
    """
    Validate ``value`` against active ``LookupOption`` rows for ``category``.

    Empty string is allowed for optional fields (caller decides).
    """
    if value is None or value == "":
        return ""
    normalized = str(value).strip()
    exists = LookupOption.objects.filter(
        category=category, value=normalized, is_active=True
    ).exists()
    if not exists:
        raise DjangoValidationError(
            {field: f"'{normalized}' is not a valid {category} option."}
        )
    return normalized
