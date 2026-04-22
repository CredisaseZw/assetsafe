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
        "closure_confirmed",
        "agreement_start_date",
        "agreement_end_date",
    )
    search_fields = (
        "agreement_number",
        "purchaser_individual__first_name",
        "purchaser_individual__last_name",
        "purchaser_company__branch_name",
        "purchaser_company__company__registration_name",
        "financier__username",
    )
    readonly_fields = (
        "purchaser",
        "balance",
        "lodge_date",
        "closure_confirmed_at",
        "date_created",
        "date_updated",
        "updated_by",
        "created_by",
    )
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
                    "purchaser_individual",
                    "purchaser_company",
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
                    "date_created",
                    "date_updated",
                    "updated_by",
                    "created_by",
                ),
                "classes": ("collapse",),
            },
        ),
    )
