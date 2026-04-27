"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""

from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

admin.site.site_header = "Assetsafe Admin"
admin.site.site_title = "Admin Portal"
admin.site.index_title = "Welcome to Assetsafe Admin Dashboard"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("apps.users.api.urls")),
    path("api/audit-log/", include("apps.users.api.audit_urls")),
    path("api/individuals/", include("apps.individuals.api.urls")),
    path("api/companies/", include("apps.companies.api.urls")),
    path("api/clients/", include("apps.clients.api.urls")),
    path("api/asset-management/", include("apps.asset_management.api.urls")),
    path("api/hire-purchase/", include("apps.hire_purchase.api.urls")),
    path("api/collateral/", include("apps.collateral.api.urls")),
    path("api/common/", include("apps.common.api.urls")),
    # API Documentation URLs
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    # Swagger UI
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    # ReDoc UI
    path(
        "api/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]
