import jsonfield
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.notification import constants
from core.models import mixins


# Model Notification.
class Notification(mixins.UUIDPkMixin,
                   mixins.ActivableMixin,
                   mixins.DateTimeManagementMixin,
                   models.Model):
    class Meta:
        verbose_name = _('Notification')
        verbose_name_plural = _('Notifications')

    title = models.CharField(
        verbose_name=_('title'),
        max_length=255,
        null=False,
        blank=False,
    )

    type = models.CharField(
        verbose_name=_('type'),
        max_length=255,
        null=False,
        blank=False,
    )

    broker_type = models.CharField(
        verbose_name=_('broker type'),
        choices=constants.BROTKER_TYPES,
        default=constants.BROKER_TYPE_ONESIGNAL,
        max_length=10,
        null=False,
        blank=False,
    )

    text = models.CharField(
        verbose_name=_('text'),
        max_length=255,
        null=False,
        blank=False,
    )

    subscriber = models.ForeignKey(
        to='notification.Subscriber',
        on_delete=models.CASCADE,
        related_name='notifications',
        null=False,
        blank=False,
    )

    extra_data = jsonfield.JSONField(
        blank=True,
        null=True
    )

    def __str__(self):
        return f'{self.subscriber} - {self.title}'
