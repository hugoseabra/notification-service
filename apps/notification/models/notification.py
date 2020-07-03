import jsonfield
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.notification import constants
from core.models import mixins


# Model Notification.
class Notification(mixins.UUIDPkMixin,
                   mixins.ActivableMixin,
                   mixins.DateTimeManagementMixin,
                   mixins.EntityMixin,
                   mixins.DomainRuleMixin,
                   mixins.DeletableModelMixin,
                   models.Model):
    class Meta:
        verbose_name = _('Notification')
        verbose_name_plural = _('Notifications')

    namespace = models.ForeignKey(
        to='notification.Namespace',
        on_delete=models.CASCADE,
        related_name='notifications',
        null=False,
        blank=False,
    )

    language = models.CharField(
        verbose_name=_('language'),
        choices=constants.NOTIFICATION_LANGUAGES,
        default=constants.NOTIFICATION_LANG_PT,
        max_length=3,
        null=False,
        blank=False
    )

    title = models.CharField(
        verbose_name=_('title'),
        max_length=255,
        null=False,
        blank=False,
    )

    url = models.CharField(
        verbose_name=_('url'),
        max_length=255,
        null=True,
        blank=True,
    )

    type = models.CharField(
        verbose_name=_('type'),
        max_length=255,
        null=False,
        blank=False,
    )

    broker_id = models.TextField(
        verbose_name=_('broker id'),
        db_index=True,
        null=True,
        blank=True,
    )

    text = models.CharField(
        verbose_name=_('text'),
        max_length=255,
        null=False,
        blank=False,
    )

    groups = models.ManyToManyField(
        to='notification.Group',
        verbose_name=_('groups'),
        related_name='notifications',
        blank=True,
    )

    extra_data = jsonfield.JSONField(
        blank=True,
        null=True
    )

    def __str__(self):
        return f'{self.namespace} - {self.title}'
