from django.contrib import admin
from .models import CollateralRegistration


@admin.register(CollateralRegistration)
class CollateralRegistrationAdmin(admin.ModelAdmin):
    list_display = (
        "agreement_number",
        "financier_display",
        "debtor_display",
        "total_debt",
        "balance",
        "is_discharged",
        "lodge_date",
    )
    list_filter = (
        "asset_type",
        "financier_type",
        "individual_financier",
        "company_financier",
        "debtor_type",
        "individual_debtor",
        "company_debtor",
        "is_discharged",
        "agreement_start_date",
        "agreement_end_date",
    )
    search_fields = (
        "agreement_number",
        "individual_financier__first_name",
        "individual_financier__last_name",
        "individual_financier__identification_number",
        "company_financier__branch_name",
        "company_financier__company__registration_name",
        "company_financier__company__trading_name",
        "individual_debtor__first_name",
        "individual_debtor__last_name",
        "individual_debtor__identification_number",
        "company_debtor__branch_name",
        "company_debtor__company__registration_name",
        "company_debtor__company__trading_name",
        "asset_registration_number",
        "chassis_number",
        "serial_number",
    )
    list_select_related = (
        "individual_financier",
        "company_financier",
        "company_financier__company",
        "individual_debtor",
        "company_debtor",
        "company_debtor__company",
        "currency",
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
                    "individual_financier",
                    "company_financier",
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
                    "individual_debtor",
                    "company_debtor",
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

    @admin.display(description="Financier")
    def financier_display(self, obj: CollateralRegistration) -> str:
        return obj.financier_display

    @admin.display(description="Debtor")
    def debtor_display(self, obj: CollateralRegistration) -> str:
        return obj.debtor_display
