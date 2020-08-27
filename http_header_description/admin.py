from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import HttpHeaderDescription
from . import resources

@admin.register(HttpHeaderDescription)
class DomainAdmin(ImportExportModelAdmin):
    resource_class = resources.HttpHeaderDescriptionResource

    list_display = (
        'id', 'name', 'description', 'updated_at', 'created_at'
    )
    list_display_links = (
        'id', 'name', 'description', 'updated_at', 'created_at'
    )
    list_filter = ('name', 'description')
    list_per_page = 25
