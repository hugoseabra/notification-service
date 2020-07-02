from rest_framework import serializers

from .device import DeviceSerializer
from .notification import NotificationSerializer
from .. import forms


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

    def to_representation(self, instance: forms.TransmissionForm.Meta.model):
        rep = super().to_representation(instance)

        device_serializer = DeviceSerializer(instance=instance.device)
        rep['device'] = device_serializer.data

        notification_serializer = NotificationSerializer(
            instance=instance.notification
        )
        rep['notification'] = notification_serializer.data

        return rep
