from django.db import models

from django.utils.translation import gettext_lazy as _

from core.models.mixins import UUIDPkMixin, DateTimeManagementMixin, ActivableMixin, EntityModelMixin 

# Model Namespace.
class Namespace(UUIDPkMixin, ActivableMixin, DateTimeManagementMixin, models.Model):
    class Meta:
        verbose_name = _('Namespace')
        verbose_name_plural = _('Namespace')

    name = models.CharField(
        verbose_name=_('name'),
        max_length=255,
        null=False,
        blank=False,
    )

    external_id = models.IntegerField(
        verbose_name=_('external id'),
        db_index=True,
        unique=True,
        null=True,
        blank=True,
    )

    description = models.CharField(
        verbose_name=_('description'),
        max_length=255,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name