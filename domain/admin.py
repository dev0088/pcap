from django.contrib import admin
from .models import Domain

@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'description', 'updated_at', 'created_at'
    )
    list_display_links = (
        'id', 'name', 'description', 'updated_at', 'created_at'
    )
    list_filter = ('name', )
    list_per_page = 25
