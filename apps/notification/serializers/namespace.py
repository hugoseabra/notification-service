from rest_framework import serializers

from core.serializers import FormSerializerMixin
from .. import forms


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
