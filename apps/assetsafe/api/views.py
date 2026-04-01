"""
views.py — AssetSafe

"""

from __future__ import annotations

from django.db.models import Count, Q, QuerySet
from django.utils import timezone
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend

from apps.assetsafe.models.models import (
    AssetRegistration,
    CollateralRegistration,
    HirePurchaseRegistration,
)
from .serializers import (
    AssetRegistrationSerializer,
    AssetRegistryDashboardSerializer,
    CollateralDashboardSerializer,
    CollateralDischargeSerializer,
    CollateralRegistrationSerializer,
    HirePurchaseClosureSerializer,
    HirePurchaseDashboardSerializer,
    HirePurchaseRegistrationSerializer,
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
        from django.db.models import Sum

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


# ---------------------------------------------------------------------------
# Collateral Registry ViewSet
# ---------------------------------------------------------------------------


class CollateralRegistrationViewSet(viewsets.ModelViewSet):
    """
    CRUD ViewSet for the Collateral Registry .
    """

    serializer_class = CollateralRegistrationSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields: list[str] = [
        "asset_type",
        "financier",
        "debtor",
        "is_discharged",
        "currency",
        "financier_type",
        "debtor_type",
    ]
    search_fields: list[str] = [
        "agreement_number",
        "debtor__username",
        "debtor__first_name",
        "debtor__last_name",
        "serial_number",
        "asset_registration_number",
        "chassis_number",
        "financier__username",
        "financier__first_name",
        "financier__last_name",
    ]
    ordering_fields: list[str] = [
        "lodge_date",
        "agreement_start_date",
        "agreement_end_date",
        "total_debt",
    ]
    ordering: list[str] = ["-lodge_date"]

    def get_queryset(self) -> QuerySet[CollateralRegistration]:
        """
        Returns all collateral records with ``financier`` and ``debtor``
        eagerly loaded via ``select_related`` to prevent N+1 queries when
        the serializer renders both ``*_display`` fields on a list response.
        """
        return CollateralRegistration.objects.select_related(
            "financier", "debtor"
        ).all()

    # ------------------------------------------------------------------
    # Custom actions
    # ------------------------------------------------------------------

    @action(detail=True, methods=["patch"], url_path="discharge")
    def discharge(self, request: Request, pk: int | None = None) -> Response:
        """
        Marks a collateral record as officially discharged.

        A dedicated ``CollateralDischargeSerializer`` is used so that this
        PATCH endpoint is scoped to only the ``is_discharged`` flag.  This
        prevents a client from accidentally overwriting unrelated fields (e.g.,
        ``total_debt``) by piggybacking on a discharge call.

        The serializer's ``update()`` method automatically stamps
        ``discharge_confirmed_at`` to guard against a client supplying a
        fabricated timestamp.
        """
        instance: CollateralRegistration = self.get_object()
        serializer = CollateralDischargeSerializer(
            instance,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_path="dashboard")
    def dashboard(self, request: Request) -> Response:
        """
        Returns the two headline statistics shown at the top of the Collateral

        """
        today = timezone.now().date()
        aggregates: dict = CollateralRegistration.objects.aggregate(
            active_agreements=Count(
                "id",
                filter=Q(
                    agreement_start_date__lte=today,
                    agreement_end_date__gte=today,
                ),
            ),
            pending_discharge_confirmation=Count(
                "id",
                filter=Q(
                    agreement_end_date__lt=today,
                    is_discharged=False,
                ),
            ),
        )

        serializer = CollateralDashboardSerializer(data=aggregates)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# ---------------------------------------------------------------------------
# Hire Purchase Registry ViewSet
# ---------------------------------------------------------------------------


class HirePurchaseRegistrationViewSet(viewsets.ModelViewSet):
    """
    CRUD ViewSet for the Hire Purchase Registry.
    """

    serializer_class = HirePurchaseRegistrationSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields: list[str] = [
        "asset_type",
        "financier",
        "purchaser",
        "purchaser_type",
        "closure_confirmed",
        "currency",
    ]
    search_fields: list[str] = [
        "agreement_number",
        "purchaser__username",
        "purchaser__first_name",
        "purchaser__last_name",
        "serial_number",
        "mv_registration_number",
        "chassis_number",
        "financier__username",
        "financier__first_name",
        "financier__last_name",
        "make",
        "model",
    ]
    ordering_fields: list[str] = [
        "lodge_date",
        "agreement_start_date",
        "agreement_end_date",
        "purchase_amount",
    ]
    ordering: list[str] = ["-lodge_date"]

    def get_queryset(self) -> QuerySet[HirePurchaseRegistration]:
        """
        Returns all HP records with ``financier`` and ``purchaser`` eagerly
        loaded via ``select_related`` to eliminate N+1 queries during
        list serialisation.
        """
        return HirePurchaseRegistration.objects.select_related(
            "financier", "purchaser"
        ).all()

    # ------------------------------------------------------------------
    # Custom actions
    # ------------------------------------------------------------------

    @action(detail=True, methods=["patch"], url_path="confirm-closure")
    def confirm_closure(self, request: Request, pk: int | None = None) -> Response:
        """
        Allows a financier to confirm that an HP agreement has closed.

        A dedicated ``HirePurchaseClosureSerializer`` limits the writable
        surface to the ``closure_confirmed`` flag only, preventing
        unintentional overwrites of other fields.

        The serializer's ``update()`` method stamps ``closure_confirmed_at``
        server-side, removing any possibility of a client supplying a
        fabricated closure timestamp.
        """
        instance: HirePurchaseRegistration = self.get_object()
        serializer = HirePurchaseClosureSerializer(
            instance,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_path="dashboard")
    def dashboard(self, request: Request) -> Response:
        """
        Returns the three headline statistics shown at the top of the HP
        """
        today = timezone.now().date()

        # Single aggregate call for the two count metrics.
        aggregates: dict = HirePurchaseRegistration.objects.aggregate(
            active_agreements=Count(
                "id",
                filter=Q(agreement_end_date__gte=today),
            ),
            pending_closure_confirmation=Count(
                "id",
                filter=Q(
                    agreement_end_date__lt=today,
                    closure_confirmed=False,
                ),
            ),
        )

        # Distinct-financier count: cannot be folded into the aggregate above
        # without a subquery, so a second lightweight query is used.
        number_of_financiers: int = (
            HirePurchaseRegistration.objects.values("financier_id").distinct().count()
        )

        serializer = HirePurchaseDashboardSerializer(
            data={
                **aggregates,
                "number_of_financiers": number_of_financiers,
            }
        )
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
