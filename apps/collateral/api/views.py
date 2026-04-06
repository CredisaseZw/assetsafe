"""
views.py — Collateral

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
from apps.collateral.models.models import CollateralRegistration
from .serializers import (
    CollateralDashboardSerializer,
    CollateralDischargeSerializer,
    CollateralRegistrationSerializer,
)


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
