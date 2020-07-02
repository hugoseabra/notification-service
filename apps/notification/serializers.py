from rest_framework import serializers

from core.serializers import FormSerializerMixin
from core.util.uuid import get_validated_uuid_from_string
from . import forms
from .models import Group


class NamespaceSerializer(FormSerializerMixin, serializers.ModelSerializer):
    class Meta:
        form = forms.NamespaceForm
        model = forms.NamespaceForm.Meta.model
        fields = (
            'pk',
            'name',
            'active',
            'external_id',
            'broker_type',
            'broker_app_id',
            'description',
            'created_at',
            'updated_at',
        )


class GroupSerializer(FormSerializerMixin, serializers.ModelSerializer):
    class Meta:
        form = forms.GroupForm
        model = forms.GroupForm.Meta.model
        fields = (
            'pk',
            'name',
            'alias',
            'active',
            'created_at',
            'updated_at',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.namespace_pk = None

    def get_form(self, data=None, files=None, **kwargs):
        if data:
            data.update({'namespace': self.namespace_pk})
        return super().get_form(data, files, **kwargs)

    def to_representation(self, instance: forms.GroupForm.Meta.model):
        rep = super().to_representation(instance)

        if self.is_requested_field('namespace'):
            namespace_serializer = NamespaceSerializer(
                instance=instance.namespace
            )
            rep['namespace'] = namespace_serializer.data

        return rep


class SubscriberSerializer(FormSerializerMixin, serializers.ModelSerializer):
    class Meta:
        form = forms.SubscriberForm
        model = forms.SubscriberForm.Meta.model
        fields = (
            'pk',
            'name',
            'active',
            'user',
            'namespace',
            'created_at',
            'updated_at',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.groups = list()

    def to_internal_value(self, data: dict):
        if 'groups' in data and isinstance(data['groups'], list):
            for group in data['groups']:
                pk = None

                if isinstance(group, dict):
                    pk = group.get('pk', None)
                elif isinstance(group, str):
                    pk = group

                pk = get_validated_uuid_from_string(pk)
                if not pk:
                    continue

                try:
                    self.groups.append(Group.objects.get(pk=pk))
                except Group.DoesNotExist:
                    pass

        data = super().to_internal_value(data)

        return data

    def get_form(self, data=None, files=None, **kwargs):
        form = super().get_form(data, files, **kwargs)

        for group in self.groups:
            form.add_group(group)

        return form

    def to_representation(self, instance: forms.GroupForm.Meta.model):
        rep = super().to_representation(instance)

        if self.is_requested_field('namespace'):
            namespace_serializer = NamespaceSerializer(
                instance=instance.namespace
            )
            rep['namespace'] = namespace_serializer.data

        if self.is_requested_field('groups') is True:
            rep['groups'] = list()
            for group in instance.groups.all():
                group_serializer = GroupSerializer(instance=group)
                rep['groups'].append(group_serializer.data)

        return rep


class DeviceSerializer(FormSerializerMixin, serializers.ModelSerializer):
    class Meta:
        form = forms.DeviceForm
        model = forms.DeviceForm.Meta.model
        fields = (
            'pk',
            'name',
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
            'subscriber',
            'active',
            'created_at',
            'updated_at',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.subscribe_pk = None

    def get_form(self, data=None, files=None, **kwargs):
        if data:
            data.update({'subscribe': self.subscribe_pk})
        return super().get_form(data, files, **kwargs)

    def to_representation(self, instance: forms.DeviceForm.Meta.model):
        rep = super().to_representation(instance)

        if self.is_requested_field('subscriber'):
            subscriber_serializer = SubscriberSerializer(
                instance=instance.subscriber
            )
            rep['subscriber'] = subscriber_serializer.data

        return rep


class NotificationSerializer(FormSerializerMixin, serializers.ModelSerializer):
    class Meta:
        form = forms.NotificationForm
        model = forms.NotificationForm.Meta.model
        fields = (
            'pk',
            'type',
            'text',
            'active',
            'language',
            'title',
            'url',
            'subscriber',
            'extra_data',
            'broker_id',
            'created_at',
            'updated_at',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.subscribe_pk = None

    def get_form(self, data=None, files=None, **kwargs):
        if data:
            data.update({'subscribe': self.subscribe_pk})
        return super().get_form(data, files, **kwargs)

    def to_representation(self, instance: forms.NotificationForm.Meta.model):
        rep = super().to_representation(instance)

        if self.is_requested_field('subscriber'):
            subscriber_serializer = SubscriberSerializer(
                instance=instance.subscriber
            )
            rep['subscriber'] = subscriber_serializer.data

        return rep


class TransmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = forms.TransmissionForm.Meta.model
        fields = (
            'pk',
            'device',
            'notification',
            'status',
            'processed_at',
            'created_at',
            'updated_at',
        )
