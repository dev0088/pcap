from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import HttpHeaderValueDescription
from . import resources

@admin.register(HttpHeaderValueDescription)
class DomainAdmin(ImportExportModelAdmin):
    resource_class = resources.HttpHeaderValueDescriptionResource

    list_display = (
        'id', 'name', 'value', 'description', 'updated_at', 'created_at'
    )
    list_display_links = (
        'id', 'name', 'value', 'description', 'updated_at', 'created_at'
    )
    list_filter = ('name', 'value', 'description')
    list_per_page = 25
