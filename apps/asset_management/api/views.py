"""
views.py — Asset Management

"""

from __future__ import annotations

import logging

from django.db.models import Count, QuerySet, Sum
from django.utils import timezone
from rest_framework import filters, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend

from apps.asset_management.models import AssetRegistration
from apps.common.api.views import BaseViewSet
from apps.users.services.audit_service import create_audit_log
from .serializers import (
    AssetRegistrationSerializer,
    AssetRegistrationListSerializer,
    AssetRegistryDashboardSerializer,
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Shared pagination
# ---------------------------------------------------------------------------


class StandardResultsSetPagination(PageNumberPagination):
    """
    Default pagination applied to every list endpoint.

    Clients may request up to ``max_page_size`` records per page by supplying
    the ``page_size`` query parameter.  Hard-capping at 100 prevents accidental
    full-table dumps via the API.
    """

    page_size: int = 25
    page_size_query_param: str = "page_size"
    max_page_size: int = 100


# ---------------------------------------------------------------------------
# Asset Registry ViewSet
# ---------------------------------------------------------------------------


class AssetRegistrationViewSet(BaseViewSet):
    """
    CRUD ViewSet for the Asset Registry .
    """

    serializer_class = AssetRegistrationSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    pagination_class = StandardResultsSetPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    # Explicit allow-list prevents consumers from filtering on arbitrary columns.
    filterset_fields: list[str] = [
        "asset_type",
        "owner_type",
        "condition",
        "currency",
    ]

    # Full-text search across the most commonly queried identifier columns.
    search_fields: list[str] = [
        "registration_number",
        "individual_owner__first_name",
        "individual_owner__last_name",
        "individual_owner__identification_number",
        "company_owner__branch_name",
        "company_owner__company__registration_name",
        "company_owner__company__trading_name",
        "serial_number",
        "mv_registration_number",
        "make",
        "model",
    ]

    ordering_fields: list[str] = [
        "lodge_date",
        "subscription_start_date",
        "subscription_end_date",
        "estimated_value",
    ]
    ordering: list[str] = ["-lodge_date"]

    def get_serializer_class(self):
        """
        Return the appropriate serializer class based on the requested action.
        We return the lighter ListSerializer for list actions for performance.
        """
        if self.action == "list":
            return AssetRegistrationListSerializer
        return super().get_serializer_class()

    def get_queryset(self) -> QuerySet[AssetRegistration]:
        """
        Returns the base queryset for this ViewSet.

        ``select_related(...)`` is always applied to prevent N+1 queries when
        the serializer renders ``owner_display`` on a list of records.

        By default, only records with an active subscription window are returned,
        matching the dashboard's "Active Agreements" view.  Clients can pass
        ``?show_all=true`` to include expired records (e.g., for an audit search).
        """
        queryset: QuerySet[AssetRegistration] = (
            AssetRegistration.objects.select_related(
                "individual_owner",
                "company_owner",
                "company_owner__company",
            ).all()
        )

        show_all: bool = (
            self.request.query_params.get("show_all", "false").lower() == "true"
        )
        if not show_all:
            today = timezone.now().date()
            queryset = queryset.filter(
                subscription_start_date__lte=today,
                subscription_end_date__gte=today,
            )

        return queryset

    # ------------------------------------------------------------------
    # Audit-logged CRUD hooks
    # ------------------------------------------------------------------

    def perform_create(self, serializer):
        super().perform_create(serializer)
        instance = serializer.instance
        create_audit_log(
            request=self.request,
            action="asset_registration.create",
            resource_type="AssetRegistration",
            resource_id=instance.pk,
            details={"registration_number": str(instance.registration_number)},
            logger=logger,
        )

    def perform_update(self, serializer):
        super().perform_update(serializer)
        instance = serializer.instance
        create_audit_log(
            request=self.request,
            action="asset_registration.update",
            resource_type="AssetRegistration",
            resource_id=instance.pk,
            details={"registration_number": str(instance.registration_number)},
            logger=logger,
        )

    def perform_destroy(self, instance):
        resource_id = instance.pk
        registration_number = str(instance.registration_number)
        super().perform_destroy(instance)
        create_audit_log(
            request=self.request,
            action="asset_registration.delete",
            resource_type="AssetRegistration",
            resource_id=resource_id,
            details={"registration_number": registration_number},
            logger=logger,
        )

    # ------------------------------------------------------------------
    # Custom actions
    # ------------------------------------------------------------------

    @action(detail=False, methods=["get"], url_path="stats")
    def stats(self, request: Request) -> Response:
        """
        Returns the two headline statistics shown at the top of the Asset
        Registry dashboard: total active asset count and their combined
        estimated value.
        """
        today = timezone.now().date()
        active_qs: QuerySet[AssetRegistration] = AssetRegistration.objects.filter(
            subscription_start_date__lte=today,
            subscription_end_date__gte=today,
        )
        aggregates: dict = active_qs.aggregate(
            total_assets=Count("id"),
            total_estimate_value=Sum("estimated_value"),
        )

        serializer = AssetRegistryDashboardSerializer(
            data={
                "total_assets": aggregates["total_assets"] or 0,
                "total_estimate_value": aggregates["total_estimate_value"] or 0,
            }
        )
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
