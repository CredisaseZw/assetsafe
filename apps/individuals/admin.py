from django.contrib import admin
from apps.individuals.models.models import (
    Individual,
    EmploymentDetail,
    IndividualAccounts,
    NextOfKin,
    IndividualContactDetail,
)
from django.utils.translation import gettext_lazy as _
from apps.common.admin import AddressInline, DocumentInline, NoteInline


@admin.register(EmploymentDetail)
class EmploymentDetailAdmin(admin.ModelAdmin):
    list_display = (
        "individual",
        "job_title",
        "employer_name",
        "industry",
        "start_date",
        "end_date",
        "is_current",
    )
    list_display_links = ("individual", "job_title")
    list_filter = ("individual", "is_current")
    search_fields = (
        "individual__first_name",
        "individual__last_name",
        "job_title",
        "employer_name",
    )
    ordering = ("-start_date", "individual__last_name")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        self.list_per_page = 20
        return qs


@admin.register(NextOfKin)
class NextOfKinAdmin(admin.ModelAdmin):
    list_display = (
        "individual",
        "first_name",
        "last_name",
        "mobile_phone",
        "email",
        "relationship",
        "physical_address",
    )
    list_display_links = ("individual", "first_name", "last_name")
    list_filter = ("relationship",)
    ordering = ("last_name", "first_name")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        self.list_per_page = 20
        return qs


@admin.register(IndividualContactDetail)
class IndividualContactDetailAdmin(admin.ModelAdmin):
    list_display = ("id", "individual", "type", "phone_number")
    list_display_links = ("individual",)
    search_fields = ("individual__first_name", "individual__last_name", "phone_number")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        self.list_per_page = 20
        return qs


@admin.register(IndividualAccounts)
class IndividualAccountsAdmin(admin.ModelAdmin):
    list_display = ("id", "individual", "vat_number", "tin_number")
    list_display_links = ("individual",)
    search_fields = (
        "individual__first_name",
        "individual__last_name",
        "individual__identification_number",
        "vat_number",
        "tin_number",
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        self.list_per_page = 20
        return queryset


class EmploymentDetailInline(admin.TabularInline):
    model = EmploymentDetail
    extra = 0
    fields = (
        "job_title",
        "employer_name",
        "industry",
        "start_date",
        "end_date",
        "is_current",
    )
    show_change_link = True


class NextOfKinInline(admin.TabularInline):
    model = NextOfKin
    extra = 0
    fields = (
        "first_name",
        "last_name",
        "mobile_phone",
        "email",
        "relationship",
        "physical_address",
    )
    show_change_link = True


class ContactDetailInline(admin.TabularInline):
    model = IndividualContactDetail
    extra = 0
    fields = ("id", "type", "phone_number")
    show_change_link = True


class AccountsInline(admin.TabularInline):
    model = IndividualAccounts
    extra = 0
    fields = ("vat_number", "tin_number")
    show_change_link = True


@admin.register(Individual)
class IndividualAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "last_name",
        "first_name",
        "identification_number",
        "identification_type",
        "get_mobile_phone",
        "created_by",
        "gender",
        "date_of_birth",
        "is_verified",
        "is_active",
        "is_deleted",
        "date_created",
    )
    list_display_links = ("last_name", "first_name", "identification_number")
    list_filter = (
        "gender",
        "identification_type",
        "is_active",
        "is_verified",
        "is_deleted",
        "date_created",
    )
    search_fields = ("first_name", "last_name", "identification_number")
    ordering = ("-date_created",)
    readonly_fields = ("account_number",)
    fieldsets = (
        (None, {"fields": ("first_name", "last_name")}),
        (
            "Identification Details",
            {"fields": ("identification_type", "identification_number")},
        ),
        (
            "Additional Information",
            {"fields": ("date_of_birth", "gender", "marital_status", "account_number")},
        ),
        ("Status", {"fields": ("is_verified", "is_active", "is_deleted")}),
    )
    inlines = [
        ContactDetailInline,
        EmploymentDetailInline,
        NextOfKinInline,
        AddressInline,
        DocumentInline,
        NoteInline,
        AccountsInline,
    ]

    def get_mobile_phone(self, obj):
        if contact := obj.contact_details.filter(type="mobile").first():
            return contact.phone_number
        else:
            return (
                obj.contact_details.first().phone_number
                if obj.contact_details.exists()
                else None
            )

    get_mobile_phone.short_description = "Phone Number"

    actions = [
        "mark_as_verified",
        "mark_as_unverified",
        "activate_individuals",
        "deactivate_individuals",
    ]

    def mark_as_verified(self, request, queryset):
        updated = queryset.update(is_verified=True)
        self.message_user(request, f"{updated} Individual marked as verified.")

    mark_as_verified.short_description = _("Mark selected Individual as verified")

    def mark_as_unverified(self, request, queryset):
        updated = queryset.update(is_verified=False)
        self.message_user(request, f"{updated} Individual marked as unverified.")

    mark_as_unverified.short_description = _("Mark selected Individual as unverified")

    def activate_individuals(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} Individual activated.")

    activate_individuals.short_description = _("Activate selected Individual")

    def deactivate_individuals(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} Individual deactivated.")

    deactivate_individuals.short_description = _("Deactivate selected Individual")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        self.list_per_page = 20
        return qs
