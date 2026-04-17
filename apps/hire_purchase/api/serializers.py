"""
serializers.py — Hire Purchase API

Serializers for HirePurchaseRegistration model.
"""

from __future__ import annotations

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers

from apps.hire_purchase.models import HirePurchaseRegistration

User = get_user_model()


# ---------------------------------------------------------------------------
# Hire Purchase serializers
# ---------------------------------------------------------------------------


class HirePurchaseRegistrationSerializer(serializers.ModelSerializer):
    """
    Full read-write serializer for
    :class:`~hire_purchase.models.HirePurchaseRegistration`.
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
        fields = [
            "id",
            "financier",
            "financier_display",
            "purchaser",
            "purchaser_display",
            "purchaser_type",
            "data_date",
            "agreement_number",
            "asset_type",
            "make",
            "model",
            "year_of_make",
            "condition",
            "mv_registration_number",
            "chassis_number",
            "engine_number",
            "serial_number",
            "currency",
            "purchase_amount",
            "instalment_amount",
            "instalment_day",
            "total_paid_to_date",
            "balance",
            "agreement_start_date",
            "agreement_end_date",
            "lodge_date",
            "closure_confirmed",
            "closure_confirmed_at",
            "is_active",
            "is_pending_closure",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "lodge_date",
            "closure_confirmed_at",
            "created_at",
            "updated_at",
            "is_active",
            "is_pending_closure",
            "financier_display",
            "purchaser_display",
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
