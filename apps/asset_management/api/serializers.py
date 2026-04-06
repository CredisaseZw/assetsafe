"""
serializers.py — Asset Management API

Serializers for AssetRegistration model.
"""

from __future__ import annotations

from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import timezone
from rest_framework import serializers

from apps.common.models import BaseAssetType
from apps.asset_management.models import AssetRegistration

User = get_user_model()

_VEHICLE_ONLY_FIELDS: tuple[str, ...] = (
    "mv_registration_number",
    "chassis_number",
    "engine_number",
)


# ---------------------------------------------------------------------------
# Asset Registry serializers
# ---------------------------------------------------------------------------


class AssetRegistrationSerializer(serializers.ModelSerializer):
    """
    Full read-write serializer for :class:`~asset_management.models.AssetRegistration`.

    Read-only computed properties
    ------------------------------
    ``is_active``        — whether today is within the subscription window.
    ``owner_display``    — human-readable owner name (avoids a second lookup).
    ``registration_number`` — server-generated; clients must never supply it.
    """

    is_active = serializers.SerializerMethodField(
        read_only=True,
        help_text="True when today is within the subscription window.",
    )
    owner_display = serializers.StringRelatedField(
        source="owner",
        read_only=True,
        help_text="Human-readable owner name; for display purposes only.",
    )

    class Meta:
        model = AssetRegistration
        fields = ["__all__"]
        read_only_fields = [
            "id",
            "registration_number",
            "lodge_date",
            "created_at",
            "updated_at",
        ]

    # ------------------------------------------------------------------
    # Computed field implementations
    # ------------------------------------------------------------------

    def get_is_active(self, obj: AssetRegistration) -> bool:
        """Delegates to the model's own ``is_active()`` helper."""
        return obj.is_active()

    # ------------------------------------------------------------------
    # Field-level validation
    # ------------------------------------------------------------------

    def validate_year_of_make(self, value: int | None) -> int | None:
        """Rejects years that are clearly impossible (pre-cars or future)."""
        if value is None:
            return value
        current_year = timezone.now().year
        if not (1900 <= value <= current_year + 1):
            raise serializers.ValidationError(
                f"Year of make must be between 1900 and {current_year + 1}."
            )
        return value

    def validate_estimated_value(self, value) -> object:
        """Ensures the estimated value is a non-negative number."""
        if value < 0:
            raise serializers.ValidationError("Estimated value must be 0 or greater.")
        return value

    # ------------------------------------------------------------------
    # Cross-field validation
    # ------------------------------------------------------------------

    def validate(self, attrs: dict) -> dict:
        """
        Cross-field validation covering:
        1. Vehicle-specific fields must be empty when the asset type is not 'vehicles'.
        2. Subscription end date must be strictly after start date.
        """
        # --- 1. Vehicle-only field guard ---
        asset_type: str = attrs.get(
            "asset_type",
            getattr(self.instance, "asset_type", None),
        )
        if asset_type and asset_type != BaseAssetType.VEHICLES:
            for field_name in _VEHICLE_ONLY_FIELDS:
                if attrs.get(field_name):
                    raise serializers.ValidationError(
                        {
                            field_name: (
                                f"'{field_name}' is only valid when asset_type is 'vehicles'. "
                                "This field should be left blank for other asset types."
                            )
                        }
                    )

        # --- 2. Subscription date ordering ---
        start = attrs.get(
            "subscription_start_date",
            getattr(self.instance, "subscription_start_date", None),
        )
        end = attrs.get(
            "subscription_end_date",
            getattr(self.instance, "subscription_end_date", None),
        )
        if start and end and end <= start:
            raise serializers.ValidationError(
                {
                    "subscription_end_date": (
                        "Subscription end date must be strictly after subscription start date."
                    )
                }
            )

        return attrs

    # ------------------------------------------------------------------
    # Create — wrapped in a transaction for safe sequential numbering
    # ------------------------------------------------------------------

    @transaction.atomic
    def create(self, validated_data: dict) -> AssetRegistration:
        """
        Wraps the default create in a DB transaction so that the
        ``select_for_update`` inside ``AssetRegistration.save()`` can
        safely serialise the registration-number generation step.
        """
        return super().create(validated_data)


class AssetRegistryDashboardSerializer(serializers.Serializer):
    """
    Read-only summary statistics for the Asset Registry dashboard panel.
    """

    total_assets = serializers.IntegerField(min_value=0)
    total_estimate_value = serializers.DecimalField(max_digits=24, decimal_places=2)
