from django import forms

from apps.notification import models


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