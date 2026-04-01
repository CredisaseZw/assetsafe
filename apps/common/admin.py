
from django.utils.translation import gettext_lazy as _
# apps/common/admin.py
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from apps.common.models.models import (
    Document, Note, Country, Province, City, Suburb, Address
)

class AddressInline(GenericTabularInline):
    model = Address
    extra = 1
    fields = (
        'address_type', 'is_primary', 'street_address', 'line_2',
        'country', 'province', 'city', 'suburb', 'postal_code',
        'latitude', 'longitude'
    )
    raw_id_fields = ('country', 'province', 'city', 'suburb')

class DocumentInline(GenericTabularInline):
    model = Document
    extra = 1
    fields = ('document_type', 'file', 'description', 'is_verified')
    readonly_fields = ('date_created', 'date_updated')

class NoteInline(GenericTabularInline):
    model = Note
    extra = 1
    fields = ('author', 'content', 'is_private')
    readonly_fields = ('date_created', 'date_updated')

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'dial_code', 'currency_code', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'code')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'country', 'is_active', 'approved')
    list_filter = ('country', 'is_active', 'approved')
    search_fields = ('name', 'code')
    raw_id_fields = ('country',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'province', 'is_active')
    list_filter = ('province__country', 'province', 'is_active')
    search_fields = ('name',)
    raw_id_fields = ('province',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Suburb)
class SuburbAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'is_active')
    list_filter = ('city__province__country', 'city__province', 'city', 'is_active')
    search_fields = ('name',)
    raw_id_fields = ('city',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = (
        'content_object', 'address_type', 'is_primary',
        'street_address', 'city', 'country','date_created'
    )
    list_filter = ('address_type', 'is_primary', 'country', 'province', 'city')
    search_fields = ('street_address', 'line_2', 'postal_code')
    raw_id_fields = ('content_type', 'country', 'province', 'city', 'suburb')

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('content_object', 'document_type', 'is_verified', 'date_created')
    list_filter = ('document_type', 'is_verified')
    search_fields = ('description',)
    raw_id_fields = ('content_type',)

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('content_object', 'author', 'is_private', 'date_created')
    list_filter = ('is_private',)
    search_fields = ('content',)
    raw_id_fields = ('content_type', 'author')

