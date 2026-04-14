from django.contrib import admin
from .models import AssetRegistration


@admin.register(AssetRegistration)
class AssetRegistrationAdmin(admin.ModelAdmin):
    list_display = (
        "registration_number",
        "owner_display",
        "owner_type",
        "asset_type",
        "make",
        "model",
        "lodge_date",
    )
    list_filter = ("asset_type", "owner_type", "condition", "lodge_date")
    search_fields = (
        "registration_number",
        "individual_owner__first_name",
        "individual_owner__last_name",
        "individual_owner__identification_number",
        "company_owner__branch_name",
        "company_owner__company__registration_name",
        "company_owner__company__trading_name",
        "make",
        "model",
    )
    readonly_fields = ("registration_number", "lodge_date", "created_at", "updated_at")
    fieldsets = (
        (
            "Registration",
            {
                "fields": (
                    "registration_number",
                    "lodge_date",
                )
            },
        ),
        (
            "Owner Information",
            {
                "fields": (
                    "owner_type",
                    "individual_owner",
                    "company_owner",
                    "owner_asset_number",
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
            "General Identification",
            {
                "fields": (
                    "serial_number",
                    "currency",
                    "estimated_value",
                    "location_address",
                )
            },
        ),
        (
            "Subscription Window",
            {
                "fields": (
                    "subscription_start_date",
                    "subscription_end_date",
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

    @admin.display(description="Owner")
    def owner_display(self, obj: AssetRegistration) -> str:
        if obj.individual_owner:
            return str(obj.individual_owner)
        if obj.company_owner:
            return str(obj.company_owner)
        return "-"
