from rest_framework import serializers

from core.serializers import FormSerializerMixin
from core.util.uuid import get_validated_uuid_from_string
from .namespace import NamespaceSerializer
from .utils import get_simple_serializer_class
from .. import forms
from ..models import Group


class SubscriberSerializer(FormSerializerMixin, serializers.ModelSerializer):
    class Meta:
        form = forms.SubscriberForm
        model = forms.SubscriberForm.Meta.model
        fields = (
            'user_id',
            'name',
            'active',
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

        return super().to_internal_value(data)

    def get_form(self, data=None, files=None, **kwargs):
        if data and self.groups:
            data['groups'] = self.groups

        return super().get_form(data, files, **kwargs)

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
                group_serializer_class = get_simple_serializer_class('group')
                group_serializer = group_serializer_class(instance=group)
                rep['groups'].append(group_serializer.data)

        return rep
