"""
models.py — Collateral
"""

from __future__ import annotations

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.common.models import (
    PartyType,
    CollateralAssetType,
    AssetCondition,
    Currency,
    TimeStampedModel,
)

User = get_user_model()


class CollateralRegistration(TimeStampedModel):
    """
    An asset lodged as collateral against a loan by a financier.

    Lifecycle
    ---------
    * ``Active`` — ``agreement_start_date`` has passed and ``agreement_end_date``
      has not yet arrived.
    * ``Pending Discharge Confirmation`` — ``agreement_end_date`` has passed but
      the financier has not yet clicked "Discharge" in the system.
    * ``Discharged`` — ``is_discharged=True``; the lender has officially released
      the collateral encumbrance.

    Financial columns
    -----------------
    ``balance`` is derived (``total_debt - total_paid_to_date``) and is stored
    rather than computed so that it survives out-of-band payment updates without
    requiring a full recalculation.
    """

    # ---- Financier (the lender) ----
    financier_type = models.CharField(
        max_length=20,
        choices=PartyType.choices,
        db_index=True,
        verbose_name=_("Financier Type"),
    )
    financier = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="collateral_records_as_financier",
        db_index=True,
        verbose_name=_("Financier"),
    )
    data_source_name = models.CharField(
        max_length=200,
        verbose_name=_("Data Source Name"),
        help_text=_("Full name of the financier representative supplying this record."),
    )
    data_date = models.DateField(
        verbose_name=_("Data Date"),
        help_text=_("Date on which the financier wants the record lodged."),
    )
    position = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Position"),
        help_text=_(
            "Job title of the data-source representative within the financier organisation."
        ),
    )

    # ---- Debtor (the borrower) ----
    debtor_type = models.CharField(
        max_length=20,
        choices=PartyType.choices,
        db_index=True,
        verbose_name=_("Debtor Type"),
    )
    debtor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="collateral_records_as_debtor",
        db_index=True,
        verbose_name=_("Debtor"),
    )

    # ---- Agreement & asset details ----
    agreement_number = models.CharField(
        max_length=100,
        db_index=True,
        verbose_name=_("Agreement Number"),
        help_text=_("The loan reference number issued by the lender."),
    )
    asset_type = models.CharField(
        max_length=30,
        choices=CollateralAssetType.choices,
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
    asset_registration_number = models.CharField(
        max_length=50,
        blank=True,
        db_index=True,
        verbose_name=_("Asset Registration Number"),
        help_text=_("Vehicle registration plate, if applicable."),
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
    total_debt = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name=_("Total Debt"),
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
        help_text=_("Stored derived value: total_debt - total_paid_to_date."),
    )

    # ---- Agreement window ----
    agreement_start_date = models.DateField(
        db_index=True, verbose_name=_("Agreement Start Date")
    )
    agreement_end_date = models.DateField(
        db_index=True, verbose_name=_("Agreement End Date")
    )
    lodge_date = models.DateField(
        auto_now_add=True,
        editable=False,
        db_index=True,
        verbose_name=_("Lodge Date"),
    )

    # ---- Discharge tracking ----
    is_discharged = models.BooleanField(
        default=False,
        db_index=True,
        verbose_name=_("Is Discharged"),
        help_text=_(
            "Set to True when the financier officially releases the collateral encumbrance."
        ),
    )
    discharge_confirmed_at = models.DateTimeField(
        null=True,
        blank=True,
        editable=False,
        verbose_name=_("Discharge Confirmed At"),
    )

    class Meta:
        ordering = ["-lodge_date"]
        verbose_name = _("Collateral Registration")
        verbose_name_plural = _("Collateral Registrations")
        indexes = [
            # Dashboard active-agreement range filter.
            models.Index(
                fields=["agreement_start_date", "agreement_end_date"],
                name="col_agreement_period_idx",
            ),
            # Pending-discharge-confirmation filter: end_date passed, not yet discharged.
            models.Index(
                fields=["is_discharged", "agreement_end_date"],
                name="col_discharge_status_idx",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.agreement_number} — {self.debtor} ({self.currency} {self.total_debt})"

    # ------------------------------------------------------------------
    # Business-logic helpers
    # ------------------------------------------------------------------

    def is_active(self) -> bool:
        """Returns ``True`` when today falls within the agreement window."""
        today = timezone.now().date()
        return self.agreement_start_date <= today <= self.agreement_end_date

    def is_pending_discharge(self) -> bool:
        """
        Returns ``True`` when the agreement end date has passed but the
        financier has not yet formally discharged the debt.
        These are the records counted in the "Pending Discharge Confirmation"
        """
        return (
            timezone.now().date() > self.agreement_end_date and not self.is_discharged
        )
