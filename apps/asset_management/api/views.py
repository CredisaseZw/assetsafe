"""
views.py — Asset Management

"""

from __future__ import annotations

from django.db.models import Count, QuerySet, Sum
from django.utils import timezone
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend

from apps.asset_management.models.models import AssetRegistration
from .serializers import (
    AssetRegistrationSerializer,
    AssetRegistryDashboardSerializer,
)


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


class AssetRegistrationViewSet(viewsets.ModelViewSet):
    """
    CRUD ViewSet for the Asset Registry .
    """

    serializer_class = AssetRegistrationSerializer
    permission_classes = [IsAuthenticated]
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
        "owner",
        "condition",
        "currency",
    ]

    # Full-text search across the most commonly queried identifier columns.
    search_fields: list[str] = [
        "registration_number",
        "owner__username",
        "owner__first_name",
        "owner__last_name",
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

    def get_queryset(self) -> QuerySet[AssetRegistration]:
        """
        Returns the base queryset for this ViewSet.

        ``select_related("owner")`` is always applied to prevent an N+1 query
        when the serializer renders ``owner_display`` on a list of records.

        By default, only records with an active subscription window are returned,
        matching the dashboard's "Active Agreements" view.  Clients can pass
        ``?show_all=true`` to include expired records (e.g., for an audit search).
        """
        queryset: QuerySet[AssetRegistration] = (
            AssetRegistration.objects.select_related("owner").all()
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
    # Custom actions
    # ------------------------------------------------------------------

    @action(detail=False, methods=["get"], url_path="dashboard")
    def dashboard(self, request: Request) -> Response:
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
