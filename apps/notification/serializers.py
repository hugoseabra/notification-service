from rest_framework import serializers

from .forms import NamespaceForm, GroupForm, SubscriberForm, DeviceForm

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

class SubscriberSerializer(FormSerializerMixin, serializers.ModelSerializer):
    class Meta:
        form = SubscriberForm
        model = SubscriberForm.Meta.model
        fields =  '__all__'

class DeviceSerializer(FormSerializerMixin, serializers.ModelSerializer):
    class Meta:
        form = DeviceForm
        model = DeviceForm.Meta.model
        fields =  '__all__'