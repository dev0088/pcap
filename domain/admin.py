from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Domain
from . import resources

@admin.register(Domain)
class DomainAdmin(ImportExportModelAdmin):
    resource_class = resources.DomainResource

    list_display = (
        'id', 'name', 'description', 'updated_at', 'created_at'
    )
    list_display_links = (
        'id', 'name', 'description', 'updated_at', 'created_at'
    )
    list_filter = ('name', )
    list_per_page = 25
