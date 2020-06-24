from django.contrib import admin

from .models import Namespace, Group

from .forms import NamespaceForm, GroupForm

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
    form = NamespaceForm
    list_filter = ('active', 'created_at', 'updated_at')
    search_fields = ('name',)
    date_hierarchy = 'created_at'

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = (
        'active',
        'created_at',
        'updated_at',
        'uuid',
        'name',
        'alias',
        'namespace',
    )
    form = GroupForm
    list_filter = ('active', 'created_at', 'updated_at', 'namespace')
    search_fields = ('name',)
    date_hierarchy = 'created_at'