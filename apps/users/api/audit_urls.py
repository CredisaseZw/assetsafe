"""URL configuration for the audit-log endpoint."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.users.api.audit_views import AuditLogViewSet

router = DefaultRouter()
router.register(r"", AuditLogViewSet, basename="audit-log")

urlpatterns = [
    path("", include(router.urls)),
]
