"""
models.py — AssetSafe
"""

from __future__ import annotations

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models, transaction
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

User = get_user_model()


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


# ---------------------------------------------------------------------------
# Asset Registry
# ---------------------------------------------------------------------------


class AssetRegistration(TimeStampedModel):
    """
    An asset lodged in the Asset Registry by an individual or company.

    Purpose
    -------
    Allows the asset owner to prove ownership to third parties and aids
    recovery in cases of theft.  The record is only "active" while the
    subscription window is open.

    Registration number
    -------------------
    ``registration_number`` is an internally generated, zero-padded sequential
    identifier (e.g., ``AR000001``).  It is written exactly once on first save
    inside a serialisable DB transaction so that concurrent inserts cannot
    produce duplicates.

    Vehicle-only fields
    -------------------
    ``mv_registration_number``, ``chassis_number``, and ``engine_number`` are
    only meaningful when ``asset_type == 'vehicles'``.  They are kept ``blank``
    at the model level; the serializer enforces the conditional requirement.
    """

    registration_number = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
        db_index=True,
        verbose_name=_("Registration Number"),
        help_text=_("Internally generated sequential identifier, e.g. AR000001."),
    )
    owner_type = models.CharField(
        max_length=20,
        choices=PartyType.choices,
        db_index=True,
        verbose_name=_("Owner Type"),
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="registered_assets",
        db_index=True,
        verbose_name=_("Owner"),
        help_text=_("Must already exist as a user in the system."),
    )
    owner_asset_number = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Owner Asset Number"),
        help_text=_("Company's own internal code for this asset, if applicable."),
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

    # ---- Vehicle-specific fields ----
    mv_registration_number = models.CharField(
        max_length=50,
        blank=True,
        db_index=True,
        verbose_name=_("MV Registration Number"),
        help_text=_(
            "Number plate. Required when asset_type is 'vehicles'; grey out otherwise."
        ),
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

    # ---- General identification ----
    serial_number = models.CharField(
        max_length=100,
        blank=True,
        db_index=True,
        verbose_name=_("Serial Number"),
        help_text=_("For non-vehicle assets that carry a serial number."),
    )
    currency = models.CharField(
        max_length=10,
        choices=Currency.choices,
        verbose_name=_("Currency"),
    )
    estimated_value = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name=_("Estimated Value"),
    )
    location_address = models.TextField(
        verbose_name=_("Location Address"),
        help_text=_(
            "Physical address where the asset is normally kept. "
            "For moveable assets, use the owner's address."
        ),
    )

    # ---- Subscription window ----
    lodge_date = models.DateField(
        auto_now_add=True,
        editable=False,
        db_index=True,
        verbose_name=_("Lodge Date"),
    )
    subscription_start_date = models.DateField(
        db_index=True,
        verbose_name=_("Subscription Start Date"),
    )
    subscription_end_date = models.DateField(
        db_index=True,
        verbose_name=_("Subscription End Date"),
    )

    class Meta:
        ordering = ["-lodge_date"]
        verbose_name = _("Asset Registration")
        verbose_name_plural = _("Asset Registrations")
        indexes = [
            # Covers the active-subscription range filter used on the dashboard.
            models.Index(
                fields=["subscription_start_date", "subscription_end_date"],
                name="ar_sub_period_idx",
            ),
            # Covers owner-centric queries (e.g., all assets belonging to a company).
            models.Index(
                fields=["owner_type", "owner"],
                name="ar_owner_type_idx",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.registration_number} — {self.make} {self.model} ({self.owner})"

    # ------------------------------------------------------------------
    # Business-logic helpers
    # ------------------------------------------------------------------

    def is_active(self) -> bool:
        """Returns ``True`` when today falls within the subscription window."""
        today = timezone.now().date()
        return self.subscription_start_date <= today <= self.subscription_end_date

    # ------------------------------------------------------------------
    # Save / registration-number generation
    # ------------------------------------------------------------------

    def save(self, *args, **kwargs) -> None:
        """
        Generates ``registration_number`` on the very first save.

        The number is computed inside a ``select_for_update`` block to
        serialise concurrent inserts and prevent two requests from receiving
        the same sequence number.
        """
        if not self.registration_number:
            self.registration_number = self._generate_registration_number()
        super().save(*args, **kwargs)

    @classmethod
    def _generate_registration_number(cls) -> str:
        """
        Mints the next AR-prefixed, six-digit zero-padded sequence number.

        Must be called from within an open DB transaction (guaranteed by the
        ``save()`` override above via Django's implicit transaction wrapping,
        or explicitly via ``transaction.atomic()``).
        """
        with transaction.atomic():
            last_record = (
                cls.objects.select_for_update()
                .only("registration_number")
                .order_by("-id")
                .first()
            )
            if last_record:
                # Strip the two-character "AR" prefix and increment.
                next_seq = int(last_record.registration_number[2:]) + 1
            else:
                next_seq = 1
            return f"AR{next_seq:06d}"


# ---------------------------------------------------------------------------
# Collateral Registry
# ---------------------------------------------------------------------------


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


# ---------------------------------------------------------------------------
# Hire Purchase Registry
# ---------------------------------------------------------------------------


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
