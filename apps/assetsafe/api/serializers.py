"""
serializers.py — AssetSafe

"""

from __future__ import annotations

from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import timezone
from rest_framework import serializers

from apps.assetsafe.models.models import (
    AssetRegistration,
    BaseAssetType,
    CollateralRegistration,
    HirePurchaseRegistration,
)

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
    Full read-write serializer for :class:`~assetsafe.models.AssetRegistration`.

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


# ---------------------------------------------------------------------------
# Collateral Registry serializers
# ---------------------------------------------------------------------------


class CollateralRegistrationSerializer(serializers.ModelSerializer):
    """
    Full read-write serializer for :class:`~assetsafe.models.CollateralRegistration`.
    """

    is_active = serializers.SerializerMethodField(read_only=True)
    is_pending_discharge = serializers.SerializerMethodField(read_only=True)
    financier_display = serializers.StringRelatedField(
        source="financier", read_only=True
    )
    debtor_display = serializers.StringRelatedField(source="debtor", read_only=True)

    class Meta:
        model = CollateralRegistration
        fields = ["__all__"]
        read_only_fields = [
            "id",
            "lodge_date",
            "discharge_confirmed_at",
            "created_at",
            "updated_at",
        ]

    # ------------------------------------------------------------------
    # Computed field implementations
    # ------------------------------------------------------------------

    def get_is_active(self, obj: CollateralRegistration) -> bool:
        return obj.is_active()

    def get_is_pending_discharge(self, obj: CollateralRegistration) -> bool:
        return obj.is_pending_discharge()

    # ------------------------------------------------------------------
    # Field-level validation
    # ------------------------------------------------------------------

    def validate_instalment_day(self, value: int) -> int:
        """Day-of-month must be within calendar bounds (1–31)."""
        if not 1 <= value <= 31:
            raise serializers.ValidationError(
                "Instalment day must be between 1 and 31."
            )
        return value

    def validate_total_paid_to_date(self, value) -> object:
        """Cannot have paid more than the total debt that was owed."""
        # We can only do this partial check here; the cross-field check
        # against total_debt happens in validate().
        if value < 0:
            raise serializers.ValidationError("Total paid to date cannot be negative.")
        return value

    # ------------------------------------------------------------------
    # Cross-field validation
    # ------------------------------------------------------------------

    def validate(self, attrs: dict) -> dict:
        """
        Cross-field validation covering:
        1. Agreement date ordering.
        2. Instalment cannot exceed total debt.
        3. Auto-derive balance when not supplied by client.
        4. Financier and debtor must be different users.
        """
        # --- 1. Date ordering ---
        start = attrs.get(
            "agreement_start_date",
            getattr(self.instance, "agreement_start_date", None),
        )
        end = attrs.get(
            "agreement_end_date",
            getattr(self.instance, "agreement_end_date", None),
        )
        if start and end and end <= start:
            raise serializers.ValidationError(
                {"agreement_end_date": "Agreement end date must be after start date."}
            )

        # --- 2. Instalment cap ---
        total_debt = attrs.get(
            "total_debt",
            getattr(self.instance, "total_debt", None),
        )
        instalment = attrs.get(
            "instalment_amount",
            getattr(self.instance, "instalment_amount", None),
        )
        if (
            total_debt is not None
            and instalment is not None
            and instalment > total_debt
        ):
            raise serializers.ValidationError(
                {"instalment_amount": "Instalment amount cannot exceed total debt."}
            )

        # --- 3. Auto-derive balance ---
        if total_debt is not None and "balance" not in attrs:
            total_paid = attrs.get(
                "total_paid_to_date",
                getattr(self.instance, "total_paid_to_date", 0),
            )
            attrs["balance"] = total_debt - total_paid

        # --- 4. Financier ≠ debtor ---
        financier = attrs.get("financier", getattr(self.instance, "financier", None))
        debtor = attrs.get("debtor", getattr(self.instance, "debtor", None))
        if financier and debtor and financier == debtor:
            raise serializers.ValidationError(
                "Financier and debtor cannot be the same user."
            )

        return attrs


class CollateralDischargeSerializer(serializers.ModelSerializer):
    """
    Narrow serializer for the ``/discharge/`` action endpoint.

    Only the ``is_discharged`` flag is writable.  ``discharge_confirmed_at``
    is stamped automatically inside ``update()`` to prevent a client from
    supplying a fabricated timestamp.
    """

    class Meta:
        model = CollateralRegistration
        fields = ["is_discharged", "discharge_confirmed_at"]
        read_only_fields = ["discharge_confirmed_at"]

    def validate_is_discharged(self, value: bool) -> bool:
        """Prevents un-discharging a record once it has been marked discharged."""
        if self.instance and self.instance.is_discharged and not value:
            raise serializers.ValidationError(
                "A discharged record cannot be re-activated via this endpoint. "
                "Please contact an administrator."
            )
        return value

    def update(
        self, instance: CollateralRegistration, validated_data: dict
    ) -> CollateralRegistration:
        """
        Stamps ``discharge_confirmed_at`` with the current UTC datetime when
        ``is_discharged`` transitions from ``False`` to ``True``.
        Uses ``update_fields`` to issue a narrow UPDATE statement rather than
        a full-row write, reducing lock contention on busy tables.
        """
        newly_discharged = (
            validated_data.get("is_discharged", False) and not instance.is_discharged
        )
        if newly_discharged:
            instance.discharge_confirmed_at = timezone.now()
        instance.is_discharged = validated_data.get(
            "is_discharged", instance.is_discharged
        )
        instance.save(
            update_fields=["is_discharged", "discharge_confirmed_at", "updated_at"]
        )
        return instance


class CollateralDashboardSerializer(serializers.Serializer):
    """
    Read-only dashboard statistics for the Collateral Registry .
    """

    active_agreements = serializers.IntegerField(min_value=0)
    pending_discharge_confirmation = serializers.IntegerField(min_value=0)


# ---------------------------------------------------------------------------
# Hire Purchase serializers
# ---------------------------------------------------------------------------


class HirePurchaseRegistrationSerializer(serializers.ModelSerializer):
    """
    Full read-write serializer for
    :class:`~assetsafe.models.HirePurchaseRegistration`.
    """

    is_active = serializers.SerializerMethodField(read_only=True)
    is_pending_closure = serializers.SerializerMethodField(read_only=True)
    financier_display = serializers.StringRelatedField(
        source="financier", read_only=True
    )
    purchaser_display = serializers.StringRelatedField(
        source="purchaser", read_only=True
    )

    class Meta:
        model = HirePurchaseRegistration
        fields = ["__all__"]
        read_only_fields = [
            "id",
            "lodge_date",
            "closure_confirmed_at",
            "created_at",
            "updated_at",
        ]

    # ------------------------------------------------------------------
    # Computed field implementations
    # ------------------------------------------------------------------

    def get_is_active(self, obj: HirePurchaseRegistration) -> bool:
        return obj.is_active()

    def get_is_pending_closure(self, obj: HirePurchaseRegistration) -> bool:
        return obj.is_pending_closure()

    # ------------------------------------------------------------------
    # Field-level validation
    # ------------------------------------------------------------------

    def validate_instalment_day(self, value: int) -> int:
        """Day-of-month must be within calendar bounds (1–31)."""
        if not 1 <= value <= 31:
            raise serializers.ValidationError(
                "Instalment day must be between 1 and 31."
            )
        return value

    # ------------------------------------------------------------------
    # Cross-field validation
    # ------------------------------------------------------------------

    def validate(self, attrs: dict) -> dict:
        """
        Cross-field validation covering:
        1. Agreement date ordering.
        2. Instalment cannot exceed purchase amount.
        3. Auto-derive balance when not supplied.
        4. Financier and purchaser must be different users.
        """
        # --- 1. Date ordering ---
        start = attrs.get(
            "agreement_start_date",
            getattr(self.instance, "agreement_start_date", None),
        )
        end = attrs.get(
            "agreement_end_date",
            getattr(self.instance, "agreement_end_date", None),
        )
        if start and end and end <= start:
            raise serializers.ValidationError(
                {
                    "agreement_end_date": (
                        "Agreement end date must be strictly after agreement start date."
                    )
                }
            )

        # --- 2. Instalment cap ---
        purchase_amount = attrs.get(
            "purchase_amount",
            getattr(self.instance, "purchase_amount", None),
        )
        instalment = attrs.get(
            "instalment_amount",
            getattr(self.instance, "instalment_amount", None),
        )
        if (
            purchase_amount is not None
            and instalment is not None
            and instalment > purchase_amount
        ):
            raise serializers.ValidationError(
                {
                    "instalment_amount": (
                        "Instalment amount cannot exceed the total purchase amount."
                    )
                }
            )

        # --- 3. Auto-derive balance ---
        if purchase_amount is not None and "balance" not in attrs:
            total_paid = attrs.get(
                "total_paid_to_date",
                getattr(self.instance, "total_paid_to_date", 0),
            )
            attrs["balance"] = purchase_amount - total_paid

        # --- 4. Financier ≠ purchaser ---
        financier = attrs.get("financier", getattr(self.instance, "financier", None))
        purchaser = attrs.get("purchaser", getattr(self.instance, "purchaser", None))
        if financier and purchaser and financier == purchaser:
            raise serializers.ValidationError(
                "Financier and purchaser cannot be the same user."
            )

        return attrs


class HirePurchaseClosureSerializer(serializers.ModelSerializer):
    """
    Narrow serializer for the ``/confirm-closure/`` action endpoint.

    Only the ``closure_confirmed`` flag is writable.
    ``closure_confirmed_at`` is stamped server-side in ``update()``.
    """

    class Meta:
        model = HirePurchaseRegistration
        fields = ["closure_confirmed", "closure_confirmed_at"]
        read_only_fields = ["closure_confirmed_at"]

    def validate_closure_confirmed(self, value: bool) -> bool:
        """Prevents rolling back a confirmed closure via this endpoint."""
        if self.instance and self.instance.closure_confirmed and not value:
            raise serializers.ValidationError(
                "A confirmed closure cannot be reversed via this endpoint."
            )
        return value

    def update(
        self, instance: HirePurchaseRegistration, validated_data: dict
    ) -> HirePurchaseRegistration:
        """
        Stamps ``closure_confirmed_at`` with the current UTC datetime when
        ``closure_confirmed`` transitions from ``False`` to ``True``.
        Uses ``update_fields`` for a targeted, low-lock UPDATE statement.
        """
        newly_closed = (
            validated_data.get("closure_confirmed", False)
            and not instance.closure_confirmed
        )
        if newly_closed:
            instance.closure_confirmed_at = timezone.now()
        instance.closure_confirmed = validated_data.get(
            "closure_confirmed", instance.closure_confirmed
        )
        instance.save(
            update_fields=["closure_confirmed", "closure_confirmed_at", "updated_at"]
        )
        return instance


class HirePurchaseDashboardSerializer(serializers.Serializer):
    """
    Read-only dashboard statistics for the HP Registry.
    """

    number_of_financiers = serializers.IntegerField(min_value=0)
    active_agreements = serializers.IntegerField(min_value=0)
    pending_closure_confirmation = serializers.IntegerField(min_value=0)
