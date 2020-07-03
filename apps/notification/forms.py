from django import forms

from . import models


class NamespaceForm(forms.ModelForm):
    class Meta:
        model = models.Namespace
        fields = '__all__'


class GroupForm(forms.ModelForm):
    class Meta:
        model = models.Group
        fields = (
            'name',
            'alias',
            'active',
            'namespace',
        )


class NotificationForm(forms.ModelForm):
    class Meta:
        model = models.Notification
        fields = '__all__'

    def _post_clean(self):
        super()._post_clean()
        for group in self.cleaned_data.get('groups', []):
            if str(group.namespace_id) != str(self.instance.namespace_id):
                self.add_error(
                    'groups',
                    f'Group "{group}" is not valid for the'
                    f' Notification "{self.instance}".'
                )


class SubscriberForm(forms.ModelForm):
    class Meta:
        model = models.Subscriber
        fields = '__all__'

    def _post_clean(self):
        super()._post_clean()
        for group in self.cleaned_data.get('groups', []):
            if str(group.namespace_id) != str(self.instance.namespace_id):
                self.add_error(
                    'groups',
                    f'Group "{group.name}" is not valid for the'
                    f' Subscriber "{self.instance.name}".'
                )


class DeviceForm(forms.ModelForm):
    class Meta:
        model = models.Device
        fields = '__all__'


class TransmissionForm(forms.ModelForm):
    class Meta:
        model = models.Transmission
        fields = '__all__'
