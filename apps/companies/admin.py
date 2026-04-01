from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.db.models import Count
from django.utils.translation import gettext_lazy as _
from apps.common.admin import AddressInline, DocumentInline, NoteInline
from .models import Company, CompanyBranch, ContactPerson, CompanyProfile


class CompanyBranchInline(admin.TabularInline):
    model = CompanyBranch
    extra = 0
    fields = ('branch_name', 'is_headquarters', 'is_deleted')
    readonly_fields = ('date_created', 'date_updated')
    show_change_link = True


class ContactPersonInline(admin.TabularInline):
    model = ContactPerson
    extra = 0
    fields = ('individual', 'contact_type', 'position', 'is_primary')
    readonly_fields = ('date_created', 'date_updated')
    show_change_link = True
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('individual', 'branch')


class CompanyProfileInline(admin.StackedInline):
    model = CompanyProfile
    extra = 0
    fields = (
        ('trading_status', 'trend', 'risk_class'),
        ('mobile_phone', 'landline_phone', 'email'),
        ('website', 'vat_number', 'tin_number'),
        ('number_of_employees', 'account_number'),
        ('is_under_judicial', 'is_suspended'),
        ('twitter', 'facebook', 'instagram', 'linkedin'),
        'operations',
        'logo',
        'contact_person',
    )
    readonly_fields = ('date_created', 'date_updated')


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'registration_name', 'trading_name', 'legal_status', 
        'industry', 'is_verified', 'is_active', 'branch_count',
        'date_of_incorporation', 'created_by', 'date_created'
    )
    list_filter = (
        'legal_status', 'is_verified', 'is_active', 'is_deleted',
        'industry', 'date_of_incorporation', 'date_created'
    )
    search_fields = (
        'registration_name', 'trading_name', 'registration_number',
        'industry'
    )
    readonly_fields = ('date_created', 'date_updated', 'created_by')
    
    fieldsets = (
        (_('Basic Information'), {
            'fields': (
                ('registration_number', 'is_verified'),
                'registration_name',
                'trading_name',
                ('legal_status', 'industry'),
                'date_of_incorporation',
            )
        }),
        (_('Status'), {
            'fields': (
                ('is_active', 'is_deleted'),
            )
        }),
        (_('System Information'), {
            'fields': (
                ('created_by', 'date_created', 'date_updated'),
            ),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [
        CompanyProfileInline,
        CompanyBranchInline,
        AddressInline,
        DocumentInline,
        NoteInline,
    ]
    
    actions = ['mark_as_verified', 'mark_as_unverified', 'activate_companies', 'deactivate_companies']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('created_by').prefetch_related('branches')
    
    def branch_count(self, obj):
        count = obj.branches.count()
        if count > 0:
            url = reverse('admin:companies_companybranch_changelist')
            return format_html('<a href="{}?company__id__exact={}">{} branches</a>', url, obj.id, count)
        return '0 branches'
    branch_count.short_description = _('Branches')
    
    def created_by(self, obj):
        return obj.created_by.get_full_name() or obj.created_by.username if obj.created_by else '-'
    created_by.short_description = _('Created By')
    
    def mark_as_verified(self, request, queryset):
        updated = queryset.update(is_verified=True)
        self.message_user(request, f'{updated} companies marked as verified.')
    mark_as_verified.short_description = _('Mark selected companies as verified')
    
    def mark_as_unverified(self, request, queryset):
        updated = queryset.update(is_verified=False)
        self.message_user(request, f'{updated} companies marked as unverified.')
    mark_as_unverified.short_description = _('Mark selected companies as unverified')
    
    def activate_companies(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} companies activated.')
    activate_companies.short_description = _('Activate selected companies')
    
    def deactivate_companies(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} companies deactivated.')
    deactivate_companies.short_description = _('Deactivate selected companies')


@admin.register(CompanyBranch)
class CompanyBranchAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'branch_name', 'company_link', 'is_headquarters',
        'contact_count', 'is_deleted', 'created_by', 'date_created'
    )
    list_filter = (
        'is_headquarters', 'is_deleted', 'date_created',
        'company__legal_status', 'company__industry'
    )
    search_fields = (
        'branch_name', 'company__registration_name', 
        'company__trading_name'
    )
    readonly_fields = ('date_created', 'date_updated', 'created_by')
    
    fieldsets = (
        (_('Branch Information'), {
            'fields': (
                'company',
                'branch_name',
                'email',
                'phone',
                ('is_headquarters', 'is_deleted'),
            )
        }),
        (_('System Information'), {
            'fields': (
                ('created_by', 'date_created', 'date_updated'),
            ),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [
        ContactPersonInline,
        AddressInline,
    ]
    
    actions = ['mark_as_headquarters', 'restore_branches']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'company', 'created_by'
        ).prefetch_related('contacts')
    
    def company_link(self, obj):
        url = reverse('admin:companies_company_change', args=[obj.company.id])
        return format_html('<a href="{}">{}</a>', url, obj.company.registration_name)
    company_link.short_description = _('Company')
    
    def contact_count(self, obj):
        count = obj.contacts.count()
        if count > 0:
            url = reverse('admin:companies_contactperson_changelist')
            return format_html('<a href="{}?branch__id__exact={}">{} contacts</a>', url, obj.id, count)
        return '0 contacts'
    contact_count.short_description = _('Contacts')
    
    def created_by(self, obj):
        return obj.created_by.get_full_name() or obj.created_by.username if obj.created_by else '-'
    created_by.short_description = _('Created By')
    
    def mark_as_headquarters(self, request, queryset):
        for branch in queryset:
            CompanyBranch.objects.filter(company=branch.company, is_headquarters=True).update(is_headquarters=False)
            branch.is_headquarters = True
            branch.save()
        self.message_user(request, f'{queryset.count()} branches marked as headquarters.')
    mark_as_headquarters.short_description = _('Mark selected branches as headquarters')
    
    def restore_branches(self, request, queryset):
        updated = queryset.update(is_deleted=False)
        self.message_user(request, f'{updated} branches restored.')
    restore_branches.short_description = _('Restore selected branches')


@admin.register(ContactPerson)
class ContactPersonAdmin(admin.ModelAdmin):
    list_display = (
        'individual_name', 'branch_link', 'contact_type', 
        'position', 'is_primary', 'created_by', 'date_created'
    )
    list_filter = (
        'contact_type', 'is_primary', 'date_created',
        'branch__company__legal_status', 'branch__is_headquarters'
    )
    search_fields = (
        'individual__first_name', 'individual__last_name',
        'branch__branch_name', 'branch__company__registration_name',
        'position'
    )
    readonly_fields = ('date_created', 'date_updated', 'created_by')
    
    fieldsets = (
        (_('Contact Information'), {
            'fields': (
                'individual',
                'branch',
                ('contact_type', 'is_primary'),
                'position',
            )
        }),
        (_('System Information'), {
            'fields': (
                ('created_by', 'date_created', 'date_updated'),
            ),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_primary', 'unmark_as_primary']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'individual', 'branch', 'branch__company', 'created_by'
        )
    
    def individual_name(self, obj):
        if obj.individual:
            url = reverse('admin:individuals_individual_change', args=[obj.individual.id])
            full_name = f"{obj.individual.first_name} {obj.individual.last_name}"
            return format_html('<a href="{}">{}</a>', url, full_name)
        return _('Unnamed Contact')
    individual_name.short_description = _('Individual')
    
    def branch_link(self, obj):
        if obj.branch:
            url = reverse('admin:companies_companybranch_change', args=[obj.branch.id])
            return format_html('<a href="{}">{}</a>', url, obj.branch.branch_name)
        return '-'
    branch_link.short_description = _('Branch')
    
    def created_by(self, obj):
        if obj.created_by:
            return obj.created_by.get_full_name() or obj.created_by.username
        return '-'
    created_by.short_description = _('Created By')
    
    def mark_as_primary(self, request, queryset):
        updated = 0
        for contact in queryset:
            # Remove primary status from other contacts of the same type in the same branch
            ContactPerson.objects.filter(
                branch=contact.branch, 
                contact_type=contact.contact_type,
                is_primary=True
            ).update(is_primary=False)
            # Mark this contact as primary
            contact.is_primary = True
            contact.save()
            updated += 1
        self.message_user(request, f'{updated} contacts marked as primary.')
    mark_as_primary.short_description = _('Mark selected contacts as primary')
    
    def unmark_as_primary(self, request, queryset):
        updated = queryset.update(is_primary=False)
        self.message_user(request, f'{updated} contacts unmarked as primary.')
    unmark_as_primary.short_description = _('Unmark selected contacts as primary')


@admin.register(CompanyProfile)
class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = (
        'company_name', 'trading_status', 'account_number', 'trend', 'risk_class',
        'number_of_employees', 'is_under_judicial', 'is_suspended',
        'date_created'
    )
    list_filter = (
        'trading_status', 'trend', 'risk_class', 'is_under_judicial',
        'is_suspended', 'date_created'
    )
    search_fields = (
        'company__registration_name', 'company__trading_name',
        'email', 'website', 'vat_number', 'tin_number'
    )
    readonly_fields = ('date_created', 'date_updated', 'logo_preview')
    
    fieldsets = (
        (_('Company Status'), {
            'fields': (
                'company',
                ('trading_status', 'trend', 'risk_class'),
                ('is_under_judicial', 'is_suspended'),
            )
        }),
        (_('Contact Information'), {
            'fields': (
                ('mobile_phone', 'landline_phone'),
                'email',
                'website',
                'contact_person',
            )
        }),
        (_('Business Information'), {
            'fields': (
                ('vat_number', 'tin_number'),
                'account_number',
                'number_of_employees',
                'registration_date',
            )
        }),
        (_('Social Media'), {
            'fields': (
                ('twitter', 'facebook'),
                ('instagram', 'linkedin'),
            ),
            'classes': ('collapse',)
        }),
        (_('Additional Information'), {
            'fields': (
                'operations',
                'logo',
                'logo_preview',
            ),
            'classes': ('collapse',)
        }),
        (_('System Information'), {
            'fields': (
                ('date_created', 'date_updated'),
            ),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [
        AddressInline,
    ]
    
    actions = ['suspend_companies', 'unsuspend_companies', 'mark_high_risk']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'company', 'contact_person'
        )
    
    def company_name(self, obj):
        url = reverse('admin:companies_company_change', args=[obj.company.id])
        return format_html('<a href="{}">{}</a>', url, obj.company.registration_name)
    company_name.short_description = _('Company')
    
    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" width="100" height="100" style="object-fit: cover;" />', obj.logo.url)
        return _('No logo')
    logo_preview.short_description = _('Logo Preview')
    
    def created_by(self, obj):
        if obj.created_by:
            return obj.created_by.get_full_name() or obj.created_by.username
        return '-'
    created_by.short_description = _('Created By')
    
    def suspend_companies(self, request, queryset):
        updated = queryset.update(is_suspended=True)
        self.message_user(request, f'{updated} company profiles suspended.')
    suspend_companies.short_description = _('Suspend selected company profiles')
    
    def unsuspend_companies(self, request, queryset):
        updated = queryset.update(is_suspended=False)
        self.message_user(request, f'{updated} company profiles unsuspended.')
    unsuspend_companies.short_description = _('Unsuspend selected company profiles')
    
    def mark_high_risk(self, request, queryset):
        updated = queryset.update(risk_class='HIGH')
        self.message_user(request, f'{updated} company profiles marked as high risk.')
    mark_high_risk.short_description = _('Mark selected profiles as high risk')


admin.site.site_header = _('Company Management System')
admin.site.site_title = _('Company Admin')
admin.site.index_title = _('Welcome to Company Administration')