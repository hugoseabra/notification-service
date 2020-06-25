from rest_framework import serializers

from core.serializers import FormSerializerMixin
from . import forms


class NamespaceSerializer(FormSerializerMixin, serializers.ModelSerializer):
    class Meta:
        form = forms.NamespaceForm
        model = forms.NamespaceForm.Meta.model
        fields = '__all__'


class GroupSerializer(FormSerializerMixin, serializers.ModelSerializer):
    class Meta:
        form = forms.GroupForm
        model = forms.GroupForm.Meta.model
        fields = '__all__'


class SubscriberSerializer(FormSerializerMixin, serializers.ModelSerializer):
    class Meta:
        form = forms.SubscriberForm
        model = forms.SubscriberForm.Meta.model
        fields = '__all__'


class DeviceSerializer(FormSerializerMixin, serializers.ModelSerializer):
    class Meta:
        form = forms.DeviceForm
        model = forms.DeviceForm.Meta.model
        fields = '__all__'


class NotificationSerializer(FormSerializerMixin, serializers.ModelSerializer):
    class Meta:
        form = forms.NotificationForm
        model = forms.NotificationForm.Meta.model
        fields = '__all__'
