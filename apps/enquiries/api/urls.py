from django.urls import path

from .views import (
    AssetEnquiryLogCreateView,
    AssetEnquiryReportView,
    AssetEnquirySearchView,
    RequesterLookupView,
)

urlpatterns = [
    path("asset/log/", AssetEnquiryLogCreateView.as_view(), name="asset-enquiry-log"),
    path("asset/search/", AssetEnquirySearchView.as_view(), name="asset-enquiry-search"),
    path("asset/report/", AssetEnquiryReportView.as_view(), name="asset-enquiry-report"),
    path(
        "asset/requesters/",
        RequesterLookupView.as_view(),
        name="asset-enquiry-requesters",
    ),
]
