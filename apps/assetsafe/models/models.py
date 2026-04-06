"""
models.py — AssetSafe (Shared Models & Enums)

This module contains shared vocabulary and base classes used across all registry apps:
- TextChoices for enumerations (PartyType, AssetType variations, AssetCondition, Currency)
- Abstract base model (TimeStampedModel) for audit timestamps

The actual registry models have been moved to dedicated apps:
- apps.asset_management: AssetRegistration
- apps.hire_purchase: HirePurchaseRegistration
- apps.collateral: CollateralRegistration
"""

from __future__ import annotations

from django.db import models
from django.utils.translation import gettext_lazy as _


# ---------------------------------------------------------------------------
# Shared vocabulary — TextChoices
# ---------------------------------------------------------------------------


class PartyType(models.TextChoices):
    """Whether a party (owner / financier / debtor / purchaser) is an individual or company."""

    INDIVIDUAL = "individual", _("Individual")
    COMPANY = "company", _("Company")


class BaseAssetType(models.TextChoices):
    """Asset categories shared across all three registries"""

    COMPUTERS = "computers", _("Computers")
    MACHINERY = "machinery", _("Machinery")
    EQUIPMENT = "equipment", _("Equipment")
    VEHICLES = "vehicles", _("Vehicles")
    LAND = "land", _("Land")
    BUILDING = "building", _("Building")
    FURNITURE = "furniture", _("Furniture")
    SHARES = "shares", _("Shares")


class CollateralAssetType(models.TextChoices):
    """
    Asset categories available in the Collateral Registry.
    Extends the base set with two financing-specific categories.
    """

    COMPUTERS = "computers", _("Computers")
    MACHINERY = "machinery", _("Machinery")
    EQUIPMENT = "equipment", _("Equipment")
    VEHICLES = "vehicles", _("Vehicles")
    LAND = "land", _("Land")
    BUILDING = "building", _("Building")
    FURNITURE = "furniture", _("Furniture")
    SHARES = "shares", _("Shares")
    INVENTORY = "inventory", _("Inventory")
    ACCOUNTS_RECEIVABLE = "accounts_receivable", _("Accounts Receivable")


class AssetCondition(models.TextChoices):
    """Physical condition of an asset at the time of registration."""

    NEW = "new", _("New")
    SECOND_HAND = "second_hand", _("Second Hand")
    RECONDITIONED = "reconditioned", _("Reconditioned")
    NON_FUNCTIONING = "non_functioning", _("Non Functioning")


class Currency(models.TextChoices):
    """Supported currencies.  Extend as the product expands to new markets."""

    USD = "USD", _("US Dollar")
    ZWL = "ZWL", _("Zimbabwean Dollar")
    ZAR = "ZAR", _("South African Rand")
    GBP = "GBP", _("British Pound")
    EUR = "EUR", _("Euro")


# ---------------------------------------------------------------------------
# Abstract base model
# ---------------------------------------------------------------------------


class TimeStampedModel(models.Model):
    """
    Abstract base class that injects ``created_at`` and ``updated_at`` audit
    timestamps into every concrete subclass automatically.
    """

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True
