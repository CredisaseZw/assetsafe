from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from apps.clients.models.models import Client

class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'client_type', 'status', 'linked_entity', 'date_created')
    list_filter = ('client_type', 'status')
    search_fields = ('name', 'external_client_id')
    readonly_fields = ('date_created', 'date_modified')
    
    fieldsets = (
        (None, {
            'fields': ('name', 'client_type', 'status', 'external_client_id')
        }),
        ('Linked Entity', {
            'fields': ('client_content_type', 'client_object_id')
        }),
        ('Dates', {
            'fields': ('date_created', 'date_modified'),
            'classes': ('collapse',)
        }),
    )
    
    def linked_entity(self, obj):
        return str(obj.client_object)
    linked_entity.short_description = 'Linked Entity'

admin.site.register(Client)