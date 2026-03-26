from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django import forms
from django.db.models import Q
from apps.users.models.models import CustomUser, Role, UserSetting

class CustomUserCreationForm(forms.ModelForm):
    """A form for creating new users with all required fields."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('email', 'username')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class RoleInline(admin.TabularInline):
    model = CustomUser.roles.through
    extra = 1
    verbose_name = _("Role")
    verbose_name_plural = _("Roles")

class UserSettingInline(admin.StackedInline):
    model = UserSetting
    can_delete = False
    verbose_name_plural = _('User Settings')
    fieldsets = (
        (None, {
            'fields': ('dark_mode_enabled', 'email_notifications_enabled')
        }),
        ('Advanced', {
            'classes': ('collapse',),
            'fields': ('preferred_currency', 'extra_preferences')
        }),
    )

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 
                    'is_active', 'is_verified', 'user_type', 'last_login')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'is_verified', 
                'client__client_type', 'roles')
    search_fields = ('username', 'first_name', 'last_name', 'email', 
                    'client__name', 'client__client_object__first_name',
                    'client__client_object__last_name')
    ordering = ('-date_joined',)
    filter_horizontal = ('user_permissions',)
    inlines = [UserSettingInline, RoleInline]
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {
            'fields': ('first_name', 'last_name', 'email', 'profile_picture')
        }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'is_verified',
                    'user_permissions', 'can_send_email'),
            'classes': ('collapse',)
        }),
        (_('Important dates'), {
            'fields': ('last_login', 'date_joined', 'last_password_change'),
            'classes': ('collapse',)
        }),
        (_('Profile Linking'), {
            'fields': ('profile_content_type', 'profile_object_id'),
            'classes': ('collapse',)
        }),
        (_('Client Association'), {
            'fields': ('client',),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2',
                    'first_name', 'last_name', 'is_staff', 'is_active'),
        }),
    )
    
    readonly_fields = ('last_login', 'date_joined', 'last_password_change')
    
    actions = ['activate_users', 'deactivate_users', 'verify_users', 'send_welcome_email']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            # Non-superusers can only see users from their same client
            if request.user.client:
                return qs.filter(client=request.user.client)
            return qs.none()
        return qs
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        
        # Limit client choices based on user permissions
        if 'client' in form.base_fields and not request.user.is_superuser:
            if request.user.client:
                form.base_fields['client'].queryset = form.base_fields['client'].queryset.filter(
                    pk=request.user.client.pk
                )
            else:
                form.base_fields['client'].queryset = form.base_fields['client'].queryset.none()
        
        # Limit profile content types to Individual and Company
        if 'profile_content_type' in form.base_fields:
            form.base_fields['profile_content_type'].queryset = ContentType.objects.filter(
                Q(app_label='individuals', model='individual') |
                Q(app_label='companies', model='company')
            )
        
        return form
    
    def user_type(self, obj):
        return obj.user_type
    user_type.short_description = _('User Type')
    user_type.admin_order_field = 'client__client_type'
    
    @admin.action(description='Activate selected users')
    def activate_users(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} users were successfully activated.")
    
    @admin.action(description='Deactivate selected users')
    def deactivate_users(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} users were successfully deactivated.")
    
    @admin.action(description='Verify selected users')
    def verify_users(self, request, queryset):
        updated = queryset.update(is_verified=True)
        self.message_user(request, f"{updated} users were successfully verified.")
    
    @admin.action(description='Send welcome email to selected users')
    def send_welcome_email(self, request, queryset):
        from apps.common.services.tasks import send_notification
        for user in queryset:
            send_notification.delay(
                recipient_type='user',
                recipient_id=user.id,
                notification_type='WELCOME_EMAIL',
                context={'user': user.username},
                sender_id=request.user.id,
                template_name='welcome_email'
            )
        self.message_user(request, f"Welcome emails will be sent to {queryset.count()} users.")

class RoleAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'is_active', 'permissions_count', 'users_count')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    filter_horizontal = ('permissions',)
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'is_active')
        }),
        (_('Permissions'), {
            'fields': ('permissions',),
            'classes': ('collapse',)
        }),
    )
    
    def permissions_count(self, obj):
        return obj.permissions.count()
    permissions_count.short_description = _('Permissions Count')
    
    def users_count(self, obj):
        return obj.users.count()
    users_count.short_description = _('Users Count')

class UserSettingAdmin(admin.ModelAdmin):
    list_display = ('user', 'dark_mode_enabled', 'email_notifications_enabled')
    list_filter = ('dark_mode_enabled', 'email_notifications_enabled')
    search_fields = ('user__username', 'user__email')
    raw_id_fields = ('user',)
    
    fieldsets = (
        (None, {
            'fields': ('user', 'dark_mode_enabled', 'email_notifications_enabled')
        }),
        (_('Advanced Preferences'), {
            'fields': ('preferred_currency', 'extra_preferences'),
            'classes': ('collapse',)
        }),
    )

admin.site.unregister(Group)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(UserSetting, UserSettingAdmin)