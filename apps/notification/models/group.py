from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import mixins


# Model Group.
class Group(mixins.UUIDPkMixin,
            mixins.ActivableMixin,
            mixins.DateTimeManagementMixin,
            mixins.EntityMixin,
            mixins.DomainRuleMixin,
            mixins.DeletableModelMixin,
            models.Model):

    class Meta:
        verbose_name = _('Group')
        verbose_name_plural = _('Groups')
        unique_together = (('namespace_id', 'alias',),)

    name = models.CharField(
        verbose_name=_('name'),
        max_length=255,
        null=False,
        blank=False,
    )

    alias = models.CharField(
        verbose_name=_('alias'),
        max_length=255,
        null=False,
        blank=False,
    )

    namespace = models.ForeignKey(
        'notification.Namespace',
        on_delete=models.PROTECT,
        related_name='groups',
        null=False,
        blank=False,
    )

    def __str__(self):
        return self.name
