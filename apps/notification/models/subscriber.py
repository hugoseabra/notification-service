from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import mixins


# Model Subscriber.
class Subscriber(mixins.ActivableMixin,
                 mixins.DateTimeManagementMixin,
                 mixins.EntityMixin,
                 mixins.DomainRuleMixin,
                 mixins.DeletableModelMixin,
                 models.Model):

    class Meta:
        verbose_name = _('Subscriber')
        verbose_name_plural = _('Subscribers')

    user_id = models.UUIDField(
        verbose_name=_('user_id'),
        max_length=255,
        unique=True,
        primary_key=True,
        null=False,
        blank=False,
    )

    name = models.CharField(
        verbose_name=_('name'),
        max_length=255,
        null=False,
        blank=False,
    )

    namespace = models.ForeignKey(
        to='notification.Namespace',
        on_delete=models.PROTECT,
        verbose_name=_('namespace'),
        related_name='subscribers',
        null=False,
        blank=False,
    )

    groups = models.ManyToManyField(
        to='notification.Group',
        verbose_name=_('groups'),
        related_name='subscribers',
        blank=True,
    )

    def __str__(self):
        return self.name
