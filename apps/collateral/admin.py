from django.contrib import admin
from .models import CollateralRegistration


@admin.register(CollateralRegistration)
class CollateralRegistrationAdmin(admin.ModelAdmin):
    list_display = (
        "agreement_number",
        "financier",
        "debtor",
        "total_debt",
        "balance",
        "is_discharged",
        "lodge_date",
    )
    list_filter = (
        "asset_type",
        "financier_type",
        "debtor_type",
        "is_discharged",
        "agreement_start_date",
        "agreement_end_date",
    )
    search_fields = (
        "agreement_number",
        "financier__username",
        "debtor__username",
    )
    readonly_fields = (
        "lodge_date",
        "discharge_confirmed_at",
        "created_at",
        "updated_at",
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
                    "financier_type",
                    "financier",
                    "data_source_name",
                    "position",
                    "data_date",
                )
            },
        ),
        (
            "Debtor Information",
            {
                "fields": (
                    "debtor_type",
                    "debtor",
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
            "Asset Identification",
            {
                "fields": (
                    "asset_registration_number",
                    "chassis_number",
                    "engine_number",
                    "serial_number",
                )
            },
        ),
        (
            "Financial Terms",
            {
                "fields": (
                    "currency",
                    "total_debt",
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
            "Discharge Status",
            {
                "fields": (
                    "is_discharged",
                    "discharge_confirmed_at",
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
