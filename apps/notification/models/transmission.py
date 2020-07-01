from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.notification import constants
from core.models import mixins

from .rules import transmission_rules as rules

# Model Notification.
class Transmission(mixins.UUIDPkMixin,
                   mixins.DateTimeManagementMixin,
                   mixins.EntityMixin,
                   mixins.DomainRuleMixin,
                   mixins.DeletableModelMixin,
                   models.Model):

    integrity_rules = (
        rules.DeviceAndNotificationSameSubscriberRule,
    )

    class Meta:
        verbose_name = _('Tranmission')
        verbose_name_plural = _('Transmissions')

    device = models.ForeignKey(
        to='notification.Device',
        on_delete=models.CASCADE,
        related_name='transmissions',
        null=False,
        blank=False,
    )

    notification = models.ForeignKey(
        to='notification.Notification',
        on_delete=models.CASCADE,
        related_name='transmissions',
        null=False,
        blank=False,
    )

    status = models.CharField(
        verbose_name=_('status'),
        choices=constants.TRANSMISSION_STATUSES,
        default=constants.TRANSMISSION_STATUS_WAITING,
        max_length=10,
        null=False,
        blank=False,
    )

    processed_at = models.DateTimeField(
        verbose_name=_('processed at'),
        null=True,
        blank=True,
    )

    def __str__(self):
        return str(self.device)
