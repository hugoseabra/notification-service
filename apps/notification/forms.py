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


class SubscriberForm(forms.ModelForm):
    class Meta:
        model = models.Subscriber
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.groups = list()

    def add_group(self, group: models.Group):
        self.groups.append(group)

    def _post_clean(self):
        super()._post_clean()

        for group in self.groups:
            if str(group.namespace_id) != str(self.instance.namespace_id):
                self.add_error(
                    None,
                    f'Group "{group.name}" is not valid for the'
                    f' Subscriber "{self.instance.name}".'
                )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        for group in self.groups:
            self.instance.groups.add(group)


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
