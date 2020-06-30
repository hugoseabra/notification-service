from rest_framework import serializers

from core.serializers import FormSerializerMixin
from . import forms


class NamespaceSerializer(FormSerializerMixin, serializers.ModelSerializer):
    class Meta:
        form = forms.NamespaceForm
        model = forms.NamespaceForm.Meta.model
        fields = (
            'pk',
            'name',
            'active',
            'external_id',
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
            'created_at',
            'updated_at',
        )

class DeviceSerializer(FormSerializerMixin, serializers.ModelSerializer):
    class Meta:
        form = forms.DeviceForm
        model = forms.DeviceForm.Meta.model
        fields = (
            'pk',
            'name',
            'active',
            'created_at',
            'updated_at',
        )

class NotificationSerializer(FormSerializerMixin, serializers.ModelSerializer):
    class Meta:
        form = forms.NotificationForm
        model = forms.NotificationForm.Meta.model
        fields = (
            'pk',
            'type',
            'text',
            'active',
            'created_at',
            'updated_at',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.subscriber_pk = None

    def get_form(self, data=None, files=None, **kwargs):
        if data:
            data.update({'subscriber': self.subscriber_pk})
        return super().get_form(data, files, **kwargs)

    def to_representation(self, instance: forms.NotificationForm.Meta.model):
        rep = super().to_representation(instance)

        if self.is_requested_field('subscriber'):
            subscriber_serializer = SubscriberSerializer(
                instance=instance.subscriber
            )
            rep['subscriber'] = subscriber_serializer.data

        return rep
