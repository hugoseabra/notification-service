from django import forms

from apps.notification import models


class NamespaceForm(forms.ModelForm):
    class Meta:
        model = models.Namespace
        fields = '__all__'