"""Privacy masking helpers for Asset Enquiry reports (1404 / 1414)."""

from __future__ import annotations

import re


def _dot_pad(visible_prefix: str, visible_suffix: str, gap: int = 4) -> str:
    gap = max(gap, 2)
    if visible_suffix:
        # Surname side uses gap+1 dots to match design examples (Ge.... .....ba).
        return f"{visible_prefix}{'.' * gap} {'.' * (gap + 1)}{visible_suffix}"
    return f"{visible_prefix}{'.' * gap}"


def mask_individual_name(first_name: str, last_name: str) -> str:
    """
    First 2 letters of first name and last 2 of surname, with dots between.

    Example: George Abba → Ge.... .....ba
    """
    first = (first_name or "").strip()
    last = (last_name or "").strip()
    prefix = first[:2] if first else ""
    suffix = last[-2:] if last else ""
    if not prefix and not suffix:
        return ""
    return _dot_pad(prefix, suffix)


def mask_company_name(name: str) -> str:
    """
    First 3 letters of the company name; if multi-word, also last 2 of last word.

    Example: Rei...... (Pvt) Ltd-style → Rei......td for multi-word names.
    """
    cleaned = re.sub(r"\s+", " ", (name or "").strip())
    if not cleaned:
        return ""
    words = cleaned.split(" ")
    prefix = cleaned[:3]
    if len(words) > 1:
        suffix = words[-1][-2:] if len(words[-1]) >= 2 else words[-1]
        return _dot_pad(prefix, suffix, gap=6)
    return f"{prefix}{'.' * 6}"


def mask_identification(value: str, *, is_registration_number: bool = False) -> str:
    """
    ID → last 4 characters; company registration number → first 3 characters.
    """
    raw = (value or "").strip()
    if not raw:
        return ""
    if is_registration_number:
        return f"{raw[:3]}...."
    return f".....{raw[-4:]}" if len(raw) >= 4 else f".....{raw}"


def mask_id_reg_display(
    identification: str | None,
    registration_number: str | None = None,
) -> str:
    """
    Combine masked ID and/or reg number as shown in designs
    (e.g. ``.....0R63 / 18....``).
    """
    parts: list[str] = []
    if identification:
        parts.append(mask_identification(identification, is_registration_number=False))
    if registration_number:
        parts.append(
            mask_identification(registration_number, is_registration_number=True)
        )
    return " / ".join(parts)
