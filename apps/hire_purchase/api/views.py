"""
views.py — Hire Purchase

"""

from __future__ import annotations

from django.db.models import Count, Q, QuerySet
from django.utils import timezone
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend

from apps.asset_management.api.views import StandardResultsSetPagination
from apps.hire_purchase.models.models import HirePurchaseRegistration
from .serializers import (
    HirePurchaseClosureSerializer,
    HirePurchaseDashboardSerializer,
    HirePurchaseRegistrationSerializer,
)


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
        "purchaser_type",
        "purchaser_individual",
        "purchaser_company",
        "closure_confirmed",
        "currency",
    ]
    search_fields: list[str] = [
        "agreement_number",
        "purchaser_individual__first_name",
        "purchaser_individual__last_name",
        "purchaser_company__branch_name",
        "purchaser_company__company__trading_name",
        "purchaser_company__company__registration_name",
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
        Returns all HP records eagerly loaded via ``select_related``.
        """
        return HirePurchaseRegistration.objects.select_related(
            "financier",
            "purchaser_individual",
            "purchaser_company",
            "purchaser_company__company",
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

    @action(detail=False, methods=["get"], url_path="stats")
    def stats(self, request: Request) -> Response:
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
