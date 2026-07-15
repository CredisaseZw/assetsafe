from django.contrib import admin

from apps.enquiries.models import AssetEnquiryLog


@admin.register(AssetEnquiryLog)
class AssetEnquiryLogAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "kind",
        "client_name",
        "branch_label",
        "performed_by",
        "requester",
        "result_found",
        "date_created",
    )
    list_filter = ("kind", "result_found")
    search_fields = ("client_name", "branch_label", "search_query")
    readonly_fields = ("date_created", "date_updated")
