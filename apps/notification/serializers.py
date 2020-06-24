from rest_framework import serializers

from .forms import NamespaceForm, GroupForm

from core.serializers import FormSerializerMixin


class NamespaceSerializer(FormSerializerMixin, serializers.ModelSerializer):
    class Meta:
        form = NamespaceForm
        model = NamespaceForm.Meta.model
        fields =  '__all__'

class GroupSerializer(FormSerializerMixin, serializers.ModelSerializer):
    class Meta:
        form = GroupForm
        model = GroupForm.Meta.model
        fields =  '__all__'