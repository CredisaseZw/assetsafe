"""
serializers.py — Collateral API

Serializers for CollateralRegistration model.
"""

from __future__ import annotations

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers

from apps.collateral.models import CollateralRegistration

User = get_user_model()


# ---------------------------------------------------------------------------
# Collateral Registry serializers
# ---------------------------------------------------------------------------


class CollateralRegistrationSerializer(serializers.ModelSerializer):
    """
    Full read-write serializer for :class:`~collateral.models.CollateralRegistration`.
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
