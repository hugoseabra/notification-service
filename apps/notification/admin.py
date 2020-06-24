from django.contrib import admin

from .models import Namespace, Group, Subscriber, Device, Notification

from .forms import NamespaceForm, GroupForm, SubscriberForm, DeviceForm, NotificationForm

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

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = (
        'active',
        'created_at',
        'updated_at',
        'uuid',
        'name',
        'user',
    )
    form=SubscriberForm
    list_filter = ('active', 'created_at', 'updated_at')
    raw_id_fields = ('groups',)
    search_fields = ('name',)
    date_hierarchy = 'created_at'


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = (
        'active',
        'created_at',
        'updated_at',
        'uuid',
        'subscriber',
        'name',
        'broker_type',
        'broker_id',
        'device_type',
        'model',
        'unique_id',
        'brand',
        'os_build_number',
        'os_version',
        'os_bundle_id',
        'os_readable_version',
        'android_fringerprint',
        'android_install_time',
        'android_bootloader',
        'ios_device_token',
    )
    form = DeviceForm
    list_filter = ('active', 'created_at', 'updated_at', 'subscriber')
    search_fields = ('name',)
    date_hierarchy = 'created_at'

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        'active',
        'created_at',
        'updated_at',
        'uuid',
        'title',
        'type',
        'status',
        'text',
        'device',
        'extra_data',
    )
    form = NotificationForm
    list_filter = ('active', 'created_at', 'updated_at', 'device')
    date_hierarchy = 'created_at'