from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import mixins


# Model Namespace.
class Namespace(mixins.UUIDPkMixin,
                mixins.ActivableMixin,
                mixins.DateTimeManagementMixin,
                mixins.EntityMixin,
                mixins.DomainRuleMixin,
                mixins.DeletableModelMixin,
                models.Model):
    class Meta:
        verbose_name = _('Namespace')
        verbose_name_plural = _('Namespaces')

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
