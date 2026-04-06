from django.contrib import admin
from .models import HirePurchaseRegistration


@admin.register(HirePurchaseRegistration)
class HirePurchaseRegistrationAdmin(admin.ModelAdmin):
    list_display = (
        "agreement_number",
        "purchaser",
        "financier",
        "purchase_amount",
        "balance",
        "closure_confirmed",
        "lodge_date",
    )
    list_filter = (
        "asset_type",
        "purchaser_type",
        "closure_confirmed",
        "agreement_start_date",
        "agreement_end_date",
    )
    search_fields = (
        "agreement_number",
        "purchaser__username",
        "financier__username",
    )
    readonly_fields = ("lodge_date", "closure_confirmed_at", "created_at", "updated_at")
    fieldsets = (
        (
            "Agreement",
            {
                "fields": (
                    "agreement_number",
                    "lodge_date",
                )
            },
        ),
        (
            "Financier Information",
            {
                "fields": (
                    "financier",
                    "data_date",
                )
            },
        ),
        (
            "Purchaser Information",
            {
                "fields": (
                    "purchaser_type",
                    "purchaser",
                )
            },
        ),
        (
            "Asset Details",
            {
                "fields": (
                    "asset_type",
                    "make",
                    "model",
                    "year_of_make",
                    "condition",
                )
            },
        ),
        (
            "Vehicle Information (if applicable)",
            {
                "fields": (
                    "mv_registration_number",
                    "chassis_number",
                    "engine_number",
                )
            },
        ),
        (
            "Asset Identification",
            {
                "fields": (
                    "serial_number",
                    "currency",
                )
            },
        ),
        (
            "Financial Terms",
            {
                "fields": (
                    "purchase_amount",
                    "instalment_amount",
                    "instalment_day",
                    "total_paid_to_date",
                    "balance",
                )
            },
        ),
        (
            "Agreement Window",
            {
                "fields": (
                    "agreement_start_date",
                    "agreement_end_date",
                )
            },
        ),
        (
            "Closure Status",
            {
                "fields": (
                    "closure_confirmed",
                    "closure_confirmed_at",
                )
            },
        ),
        (
            "Audit Timestamps",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                ),
                "classes": ("collapse",),
            },
        ),
    )
