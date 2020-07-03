# -*- coding: utf-8 -*-
import jsonfield
from django.contrib import admin
from django_json_widget.widgets import JSONEditorWidget

from . import forms
from . import models


@admin.register(models.Namespace)
class NamespaceAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'active',
        'external_id',
        'broker_type',
        'broker_app_id',
        'last_process',
    )
    readonly_fields = (
        'pk',
        'created_at',
        'updated_at',
    )
    list_filter = ('active', 'created_at', 'updated_at', 'broker_type')
    search_fields = ('name', 'external_id', 'broker_app_id')
    date_hierarchy = 'created_at'
    form = forms.NamespaceForm


@admin.register(models.Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'alias',
        'namespace',
        'active',
    )
    list_filter = ('active', 'created_at', 'updated_at', 'namespace')
    readonly_fields = (
        'pk',
        'created_at',
        'updated_at',
    )
    search_fields = ('name',)
    date_hierarchy = 'created_at'
    form = forms.GroupForm


@admin.register(models.Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'user_id',
        'active',
    )
    readonly_fields = (
        'pk',
        'created_at',
        'updated_at',
    )
    list_filter = ('active', 'created_at', 'updated_at', 'namespace')
    search_fields = ('name', 'user_id')
    date_hierarchy = 'created_at'
    form = forms.SubscriberForm


@admin.register(models.Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'subscriber',
        'model',
        'active',
    )
    list_filter = (
        'active',
        'created_at',
        'updated_at',
        'subscriber',
        'subscriber__namespace',
    )
    readonly_fields = (
        'pk',
        'created_at',
        'updated_at',
    )
    search_fields = ('name',)
    date_hierarchy = 'created_at'
    form = forms.DeviceForm


@admin.register(models.Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'type',
        'namespace',
        'created_at',
    )
    readonly_fields = (
        'pk',
        'created_at',
        'updated_at',
    )
    list_filter = ('created_at', 'updated_at', 'namespace')
    date_hierarchy = 'created_at'
    form = forms.NotificationForm
    formfield_overrides = {
        jsonfield.JSONField: {'widget': JSONEditorWidget},
    }


@admin.register(models.Transmission)
class TransmissionAdmin(admin.ModelAdmin):
    list_display = (
        'device',
        'notification',
        'status',
        'processed_at',
    )
    readonly_fields = (
        'pk',
        'created_at',
        'updated_at',
    )
    list_filter = (
        'created_at',
        'updated_at',
        'device',
        'processed_at',
    )
    date_hierarchy = 'created_at'
    form = forms.TransmissionForm
