"""
models.py — Asset Management
"""

from __future__ import annotations

from django.core.validators import MinValueValidator
from django.db import models, transaction
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.common.models import (
    PartyType,
    BaseAssetType,
    AssetCondition,
    Currency,
    TimeStampedModel,
)
from apps.companies.models.models import CompanyBranch
from apps.individuals.models.models import Individual


class AssetRegistration(TimeStampedModel):
    """
    An asset lodged in the Asset Registry by an individual or company.

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
    individual_owner = models.ForeignKey(
        Individual,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Individual Owner"),
    )
    company_owner = models.ForeignKey(
        CompanyBranch,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Company Owner"),
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
    currency = models.ForeignKey(
        Currency,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
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
        verbose_name=_("Lodge Date"),
    )
    subscription_start_date = models.DateField(
        verbose_name=_("Subscription Start Date"),
    )
    subscription_end_date = models.DateField(
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
            # Covers owner-centric queries across both owner relations.
            models.Index(
                fields=["owner_type", "individual_owner"],
                name="ar_owner_ind_idx",
            ),
            models.Index(
                fields=["owner_type", "company_owner"],
                name="ar_owner_comp_idx",
            ),
        ]

    def __str__(self) -> str:
        owner = self.individual_owner or self.company_owner or _("Unassigned Owner")
        return f"{self.registration_number} — {self.make} {self.model} ({owner})"

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
