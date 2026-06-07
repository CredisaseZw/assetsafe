"""
Audit Log API view — staff-only, read-only, paginated.

GET /api/audit-log/        → paginated list of all audit log entries
GET /api/audit-log/{id}/   → single entry detail

No create, update, or delete is permitted (append-only policy).
"""

from __future__ import annotations

from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated

from apps.users.utils.permissions import IsSuperuser

from django_filters.rest_framework import DjangoFilterBackend

from apps.asset_management.api.views import StandardResultsSetPagination
from apps.users.models.audit import AuditLog
from apps.users.api.audit_serializers import AuditLogSerializer


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A read-only ViewSet that exposes the append-only audit trail.

    *   Only superusers may access this endpoint.
    *   Results are returned in reverse-chronological order (newest first).
    *   Supports filtering by ``resource_type``, ``success``, and
        ``created_by``; and ordering by ``timestamp``.
    """

    queryset = AuditLog.objects.select_related("created_by").all()
    serializer_class = AuditLogSerializer
    permission_classes = [IsAuthenticated, IsSuperuser]
    pagination_class = StandardResultsSetPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["resource_type", "success", "created_by"]
    search_fields = ["action", "resource_type", "created_by__username"]
    ordering_fields = ["timestamp"]
    ordering = ["-timestamp"]
    # Audit log is append-only — restrict HTTP verbs at the transport level.
    http_method_names = ["get", "head", "options"]
