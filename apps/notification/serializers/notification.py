from rest_framework import serializers

from core.serializers import FormSerializerMixin
from .namespace import NamespaceSerializer
from .. import forms


class NotificationSerializer(FormSerializerMixin, serializers.ModelSerializer):
    class Meta:
        form = forms.NotificationForm
        model = forms.NotificationForm.Meta.model
        fields = (
            'pk',
            'type',
            'language',
            'title',
            'text',
            'active',
            'language',
            'title',
            'url',
            'namespace',
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

        if self.is_requested_field('namespace'):
            namespace_serializer = NamespaceSerializer(
                instance=instance.namespace
            )
            rep['namespace'] = namespace_serializer.data

        return rep
