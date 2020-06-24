from rest_framework import serializers

from .forms import NamespaceForm

from core.serializers import FormSerializerMixin


class NamespaceSerializer(FormSerializerMixin, serializers.ModelSerializer):
    class Meta:
        form = NamespaceForm
        model = NamespaceForm.Meta.model
        fields =  '__all__'