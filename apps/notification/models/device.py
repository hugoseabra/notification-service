from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import mixins


# Model Device.
class Device(mixins.UUIDPkMixin,
             mixins.ActivableMixin,
             mixins.DateTimeManagementMixin,
             mixins.EntityMixin,
             mixins.DomainRuleMixin,
             mixins.DeletableModelMixin,
             models.Model):
    class Meta:
        verbose_name = _('Device')
        verbose_name_plural = _('Devices')

    subscriber = models.ForeignKey(
        to='notification.Subscriber',
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )

    name = models.CharField(
        verbose_name=_('name'),
        max_length=255,
        null=False,
        blank=False,
    )

    broker_id = models.TextField(
        verbose_name=_('broker id'),
        db_index=True,
        null=False,
        blank=False,
    )

    device_type = models.CharField(
        verbose_name=_('device type'),
        max_length=255,
        null=False,
        blank=False,
    )

    model = models.CharField(
        verbose_name=_('model'),
        max_length=255,
        null=False,
        blank=False,
    )

    unique_id = models.TextField(
        verbose_name=_('unique id'),
        db_index=True,
        unique=True,
        null=False,
        blank=False,
    )

    brand = models.CharField(
        verbose_name=_('brand'),
        max_length=255,
        null=False,
        blank=False,
    )

    os_build_number = models.TextField(
        verbose_name=_('os build number'),
        db_index=True,
        unique=True,
        null=False,
        blank=False,
    )

    os_version = models.TextField(
        verbose_name=_('os version'),
        db_index=True,
        unique=True,
        null=False,
        blank=False,
    )

    os_bundle_id = models.TextField(
        verbose_name=_('os bundle id'),
        db_index=True,
        unique=True,
        null=False,
        blank=False,
    )

    os_readable_version = models.TextField(
        verbose_name=_('os readable version'),
        db_index=True,
        unique=True,
        null=False,
        blank=False,
    )

    android_fringerprint = models.TextField(
        verbose_name=_('android fingerprint'),
        null=True,
        blank=True,
    )

    android_install_time = models.TextField(
        verbose_name=_('android install time'),
        null=True,
        blank=True,
    )

    android_bootloader = models.TextField(
        verbose_name=_('android bootloader'),
        null=True,
        blank=True,
    )

    ios_device_token = models.TextField(
        verbose_name=_('ios device token'),
        null=True,
        blank=True,
    )

    def __str__(self):
        return f'{self.subscriber} - {self.name}'
