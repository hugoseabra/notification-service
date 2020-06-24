from django.contrib import admin

from .models import Namespace


@admin.register(Namespace)
class NamespaceAdmin(admin.ModelAdmin):
    list_display = (
        'active',
        'created_at',
        'updated_at',
        'uuid',
        'name',
        'external_id',
        'description',
    )
    list_filter = ('active', 'created_at', 'updated_at')
    search_fields = ('name',)
    date_hierarchy = 'created_at'