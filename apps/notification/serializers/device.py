from rest_framework import serializers

from core.serializers import FormSerializerMixin
from .subscriber import SubscriberSerializer
from .. import forms


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
            'android_fingerprint',
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
