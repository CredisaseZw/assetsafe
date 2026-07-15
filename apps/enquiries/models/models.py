"""Asset enquiry log — tracks external (billable) enquiries for month-end invoicing."""

from __future__ import annotations

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.clients.models.models import Client
from apps.common.models.base_models import BaseModel


class EnquiryKind(models.TextChoices):
    INTERNAL = "internal", _("Internal")
    EXTERNAL = "external", _("External")


class AssetEnquiryLog(BaseModel):
    """
    Records an asset enquiry session for audit and external billing.

    External enquiries are performed by Fincheck staff on behalf of a client;
    ``requester`` is the client user, and ``client`` / ``branch_label`` are
    snapshotted for invoicing.
    """

    kind = models.CharField(
        max_length=20,
        choices=EnquiryKind.choices,
        db_index=True,
        verbose_name=_("Enquiry Kind"),
    )
    performed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="asset_enquiries_performed",
        verbose_name=_("Performed By"),
    )
    requester = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="asset_enquiries_as_requester",
        verbose_name=_("Requester"),
        help_text=_("Client-side user for external enquiries."),
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="asset_enquiries",
        verbose_name=_("Client"),
    )
    client_name = models.CharField(max_length=255, blank=True)
    branch_label = models.CharField(max_length=255, blank=True)
    search_query = models.CharField(max_length=255, blank=True)
    search_field = models.CharField(max_length=50, blank=True)
    result_found = models.BooleanField(null=True, blank=True)

    class Meta:
        app_label = "enquiries"
        ordering = ["-date_created"]
        verbose_name = _("Asset Enquiry Log")
        verbose_name_plural = _("Asset Enquiry Logs")

    def __str__(self) -> str:
        return f"{self.kind} enquiry #{self.pk}"
