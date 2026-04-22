"""
models.py — Collateral
"""

from __future__ import annotations

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.functions import Lower
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.collateral.constants import ASSET_IDENTIFIER_FIELDS, ASSET_IDENTIFIER_LABELS
from apps.common.models import (
    PartyType,
    CollateralAssetType,
    AssetCondition,
    Currency,
)
from apps.common.models.base_models import BaseModelWithUser
from apps.clients.models.models import Client
from apps.companies.models.models import CompanyBranch
from apps.individuals.models.models import Individual

DEBTOR_TYPE_INDIVIDUAL = PartyType.INDIVIDUAL.value
DEBTOR_TYPE_COMPANY = PartyType.COMPANY.value
DEBTOR_TYPE_CHOICES = PartyType.choices


class CollateralRegistration(BaseModelWithUser):
    """
    An asset lodged as collateral against a loan by a financier.

    Lifecycle
    ---------
    * ``Active`` —  ``agreement_start_date`` has passed and ``agreement_end_date``
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
    financier = models.ForeignKey(
        Client,
        on_delete=models.PROTECT,
        related_name="collateral_records_as_financier",
        verbose_name=_("Financier"),
    )
    data_date = models.DateField(
        verbose_name=_("Data Date"),
        help_text=_("Date on which the financier wants the record lodged."),
    )

    # ---- Debtor (the borrower) ----
    debtor_type = models.CharField(
        max_length=20,
        choices=DEBTOR_TYPE_CHOICES,
        db_index=True,
        verbose_name=_("Debtor Type"),
    )
    individual_debtor = models.ForeignKey(
        Individual,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="collateral_records_as_individual_debtor",
    )
    company_debtor = models.ForeignKey(
        CompanyBranch,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="collateral_records_as_company_debtor",
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
    currency = models.ForeignKey(
        Currency,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
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
        constraints = [
            models.UniqueConstraint(
                Lower("asset_registration_number"),
                condition=(
                    models.Q(is_discharged=False)
                    & ~models.Q(asset_registration_number="")
                ),
                name="col_uq_open_asset_reg_ci",
            ),
            models.UniqueConstraint(
                Lower("chassis_number"),
                condition=(
                    models.Q(is_discharged=False) & ~models.Q(chassis_number="")
                ),
                name="col_uq_open_chassis_ci",
            ),
            models.UniqueConstraint(
                Lower("serial_number"),
                condition=(models.Q(is_discharged=False) & ~models.Q(serial_number="")),
                name="col_uq_open_serial_ci",
            ),
        ]

    def __str__(self) -> str:
        return (
            f"{self.agreement_number} — {self.debtor_display} "
            f"({self.currency} {self.total_debt})"
        )

    @property
    def financier_display(self) -> str:
        if self.financier is not None:
            return str(self.financier)
        return str(_("Unassigned Financier"))

    @property
    def debtor_display(self) -> str:
        if (
            self.debtor_type == DEBTOR_TYPE_INDIVIDUAL
            and self.individual_debtor is not None
        ):
            return str(self.individual_debtor)
        if self.debtor_type == DEBTOR_TYPE_COMPANY and self.company_debtor is not None:
            return str(self.company_debtor)
        if self.individual_debtor is not None:
            return str(self.individual_debtor)
        if self.company_debtor is not None:
            return str(self.company_debtor)
        return str(_("Unassigned Debtor"))

    def _validate_party(self, role: str, errors: dict[str, object]) -> None:
        party_type = getattr(self, f"{role}_type", None)
        individual = getattr(self, f"individual_{role}", None)
        company = getattr(self, f"company_{role}", None)

        if party_type == DEBTOR_TYPE_INDIVIDUAL:
            if not individual:
                errors[f"individual_{role}"] = (
                    f"Individual {role} is required when {role}_type is 'individual'."
                )
            if company:
                errors[f"company_{role}"] = (
                    f"Company {role} must be empty when {role}_type is 'individual'."
                )
        elif party_type == DEBTOR_TYPE_COMPANY:
            if not company:
                errors[f"company_{role}"] = (
                    f"Company {role} is required when {role}_type is 'company'."
                )
            if individual:
                errors[f"individual_{role}"] = (
                    f"Individual {role} must be empty when {role}_type is 'company'."
                )

    def _validate_financier_debtor_distinct(self, errors: dict[str, object]) -> None:
        if self.financier is None:
            errors["financier"] = "Financier is required."
            return

        if (
            self.debtor_type == DEBTOR_TYPE_INDIVIDUAL
            and self.individual_debtor is not None
            and self.financier.is_individual_client
            and self.financier.linked_individual == self.individual_debtor
        ):
            errors["individual_debtor"] = (
                "Debtor cannot be the same individual as the financier."
            )

        if (
            self.debtor_type == DEBTOR_TYPE_COMPANY
            and self.company_debtor is not None
            and self.financier.is_company_client
            and self.financier.linked_company_branch == self.company_debtor
        ):
            errors["company_debtor"] = (
                "Debtor cannot be the same company as the financier."
            )

    def _validate_unique_asset_identifiers(self, errors: dict[str, object]) -> None:
        """
        Prevent duplicate open collateral registrations for the same asset.

        Duplicate checks are only enforced when ``is_discharged=False`` so an
        asset can be re-registered once the previous encumbrance has been
        discharged.
        """
        if self.is_discharged:
            return

        identifiers: dict[str, str] = {}
        for field_name in ASSET_IDENTIFIER_FIELDS:
            raw_value = getattr(self, field_name, "")
            value = raw_value.strip() if isinstance(raw_value, str) else raw_value
            if isinstance(raw_value, str):
                setattr(self, field_name, value)
            if value:
                identifiers[field_name] = value

        if not identifiers:
            return

        existing_qs = CollateralRegistration._default_manager.filter(
            is_discharged=False
        )
        if self.pk:
            existing_qs = existing_qs.exclude(pk=self.pk)

        for field_name, value in identifiers.items():
            if existing_qs.filter(**{f"{field_name}__iexact": value}).exists():
                label = ASSET_IDENTIFIER_LABELS.get(
                    field_name,
                    field_name.replace("_", " "),
                )
                errors[field_name] = (
                    f"An active collateral registration already exists with this {label}."
                )

    def clean(self) -> None:
        super().clean()

        errors: dict[str, object] = {}
        self._validate_party("debtor", errors)
        self._validate_financier_debtor_distinct(errors)

        if (
            self.agreement_start_date is not None
            and self.agreement_end_date is not None
            and self.agreement_end_date <= self.agreement_start_date
        ):
            errors["agreement_end_date"] = (
                "Agreement end date must be after start date."
            )

        if self.total_debt is not None and self.total_paid_to_date is not None:
            if self.total_paid_to_date > self.total_debt:
                errors["total_paid_to_date"] = (
                    "Total paid to date cannot exceed total debt."
                )

            expected_balance = self.total_debt - self.total_paid_to_date
            if self.balance is None:
                self.balance = expected_balance
            elif self.balance != expected_balance:
                errors["balance"] = (
                    "Balance must equal total_debt - total_paid_to_date."
                )

        self._validate_unique_asset_identifiers(errors)

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

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
