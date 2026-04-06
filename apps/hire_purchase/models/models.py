"""
models.py — Hire Purchase
"""

from __future__ import annotations

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.common.models import (
    PartyType,
    BaseAssetType,
    AssetCondition,
    Currency,
    TimeStampedModel,
)

User = get_user_model()


class HirePurchaseRegistration(TimeStampedModel):
    """
    An asset held under a Hire Purchase agreement.

    Lifecycle
    ---------
    * ``Active`` — ``agreement_end_date`` has not yet arrived.
    * ``Pending Closure Confirmation`` — ``agreement_end_date`` has passed but
      the financier has not confirmed closure (the agreement may have been
      extended without the system being updated).
    * ``Closed`` — ``closure_confirmed=True``; the financier has acknowledged
      that the agreement has ended.
    """

    # ---- Financier ----
    financier = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="hp_records_as_financier",
        db_index=True,
        verbose_name=_("Financier"),
    )
    data_date = models.DateField(
        default=timezone.now,
        verbose_name=_("Data Date"),
        help_text=_("Date the record is lodged; defaults to today."),
    )

    # ---- Purchaser (formerly "Lessee") ----
    purchaser_type = models.CharField(
        max_length=20,
        choices=PartyType.choices,
        db_index=True,
        verbose_name=_("Purchaser Type"),
    )
    purchaser = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="hp_records_as_purchaser",
        db_index=True,
        verbose_name=_("Purchaser"),
    )

    # ---- Agreement & asset details ----
    agreement_number = models.CharField(
        max_length=100,
        db_index=True,
        verbose_name=_("Agreement Number"),
        help_text=_("The financier's own agreement reference number."),
    )
    asset_type = models.CharField(
        max_length=30,
        choices=BaseAssetType.choices,
        db_index=True,
        verbose_name=_("Asset Type"),
    )
    make = models.CharField(max_length=100, blank=True, verbose_name=_("Make"))
    model = models.CharField(max_length=100, blank=True, verbose_name=_("Model"))
    year_of_make = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name=_("Year of Make"),
    )
    condition = models.CharField(
        max_length=20,
        choices=AssetCondition.choices,
        blank=True,
        verbose_name=_("Condition"),
    )
    mv_registration_number = models.CharField(
        max_length=50,
        blank=True,
        db_index=True,
        verbose_name=_("MV Registration Number"),
    )
    chassis_number = models.CharField(
        max_length=100,
        blank=True,
        db_index=True,
        verbose_name=_("Chassis Number"),
    )
    engine_number = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Engine Number"),
    )
    serial_number = models.CharField(
        max_length=100,
        blank=True,
        db_index=True,
        verbose_name=_("Serial Number"),
    )

    # ---- Financials ----
    currency = models.CharField(
        max_length=10,
        choices=Currency.choices,
        verbose_name=_("Currency"),
    )
    purchase_amount = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name=_("Purchase Amount"),
        help_text=_("Total contractual amount to be paid over the HP period."),
    )
    instalment_amount = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name=_("Instalment Amount"),
    )
    instalment_day = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(31)],
        verbose_name=_("Instalment Day"),
        help_text=_("Day-of-month (dd) when each instalment falls due."),
    )
    total_paid_to_date = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name=_("Total Paid to Date"),
    )
    balance = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name=_("Balance"),
        help_text=_("Stored derived value: purchase_amount - total_paid_to_date."),
    )

    # ---- Agreement window ----
    agreement_start_date = models.DateField(
        db_index=True,
        verbose_name=_("Agreement Start Date"),
    )
    agreement_end_date = models.DateField(
        db_index=True,
        verbose_name=_("Agreement End Date"),
    )
    lodge_date = models.DateField(
        auto_now_add=True,
        editable=False,
        db_index=True,
        verbose_name=_("Lodge Date"),
    )

    # ---- Closure tracking ----
    closure_confirmed = models.BooleanField(
        default=False,
        db_index=True,
        verbose_name=_("Closure Confirmed"),
        help_text=_(
            "Financier must actively confirm when an agreement closes. "
            "Until confirmed, an ended agreement is counted as 'Pending Closure Confirmation'."
        ),
    )
    closure_confirmed_at = models.DateTimeField(
        null=True,
        blank=True,
        editable=False,
        verbose_name=_("Closure Confirmed At"),
    )

    class Meta:
        ordering = ["-lodge_date"]
        verbose_name = _("Hire Purchase Registration")
        verbose_name_plural = _("Hire Purchase Registrations")
        indexes = [
            # Dashboard active-agreement range filter.
            models.Index(
                fields=["agreement_start_date", "agreement_end_date"],
                name="hp_agreement_period_idx",
            ),
            # Pending-closure filter.
            models.Index(
                fields=["closure_confirmed", "agreement_end_date"],
                name="hp_closure_status_idx",
            ),
            # Per-financier closure status (used by the financier search feature).
            models.Index(
                fields=["financier", "closure_confirmed"],
                name="hp_financier_closure_idx",
            ),
        ]

    def __str__(self) -> str:
        return (
            f"HP {self.agreement_number} — {self.purchaser} ({self.make} {self.model})"
        )

    # ------------------------------------------------------------------
    # Business-logic helpers
    # ------------------------------------------------------------------

    def is_active(self) -> bool:
        """Returns ``True`` when today falls within the agreement window."""
        return timezone.now().date() <= self.agreement_end_date

    def is_pending_closure(self) -> bool:
        """
        Returns ``True`` when the agreement end date has passed but closure has
        not yet been confirmed by the financier.  Corresponds to the
        "Pending Closure Confirmation" metric on the HP dashboard
        """
        return (
            timezone.now().date() > self.agreement_end_date
            and not self.closure_confirmed
        )
