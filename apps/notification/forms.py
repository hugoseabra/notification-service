from django import forms

from . import models


class NamespaceForm(forms.ModelForm):
    class Meta:
        model = models.Namespace
        fields = '__all__'


class GroupForm(forms.ModelForm):
    class Meta:
        model = models.Group
        fields = '__all__'


class SubscriberForm(forms.ModelForm):
    class Meta:
        model = models.Subscriber
        fields = '__all__'


class DeviceForm(forms.ModelForm):
    class Meta:
        model = models.Device
        fields = '__all__'


class NotificationForm(forms.ModelForm):
    class Meta:
        model = models.Notification
        fields = '__all__'


class TransmissionForm(forms.ModelForm):
    class Meta:
        model = models.Transmission
        fields = '__all__'
