from rest_framework import serializers

from core.serializers import FormSerializerMixin
from .namespace import NamespaceSerializer
from .. import forms


class SimpleGroupSerializer(FormSerializerMixin, serializers.ModelSerializer):
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


class GroupSerializer(SimpleGroupSerializer):
    def to_representation(self, instance: forms.GroupForm.Meta.model):
        rep = super().to_representation(instance)

        if self.is_requested_field('namespace'):
            namespace_serializer = NamespaceSerializer(
                instance=instance.namespace
            )
            rep['namespace'] = namespace_serializer.data

        return rep
