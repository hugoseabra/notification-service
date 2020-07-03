from rest_framework import serializers

from core.serializers import FormSerializerMixin
from core.util.uuid import get_validated_uuid_from_string
from .namespace import NamespaceSerializer
from .utils import get_simple_serializer_class
from .. import forms
from ..models import Group


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

        return super().to_internal_value(data)

    def get_form(self, data=None, files=None, **kwargs):
        if data:
            data.update({'subscribe': self.subscribe_pk})

        form = super().get_form(data, files, **kwargs)

        for group in self.groups:
            form.add_group(group)

        return form

    def to_representation(self, instance: forms.NotificationForm.Meta.model):
        rep = super().to_representation(instance)

        if self.is_requested_field('namespace'):
            namespace_serializer = NamespaceSerializer(
                instance=instance.namespace
            )
            rep['namespace'] = namespace_serializer.data

        if self.is_requested_field('groups') is True:
            rep['groups'] = list()
            for group in instance.groups.all():
                group_serializer_class = get_simple_serializer_class('group')
                group_serializer = group_serializer_class(instance=group)
                rep['groups'].append(group_serializer.data)

        return rep
