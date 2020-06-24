from django.db import models

from django.utils.translation import gettext_lazy as _

from core.models.mixins import UUIDPkMixin, DateTimeManagementMixin, ActivableMixin, EntityModelMixin 

from apps.notification import constants

import jsonfield

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

# Model Group.
class Group(UUIDPkMixin, ActivableMixin, DateTimeManagementMixin, models.Model):
    class Meta:
        verbose_name = _('Group')
        verbose_name_plural = _('Group')

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
        Namespace,
        models.DO_NOTHING,
        db_column='namespace',
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name

# Model Subscriber.
class Subscriber(UUIDPkMixin, ActivableMixin, DateTimeManagementMixin, models.Model):
    class Meta:
        verbose_name = _('Subscriber')
        verbose_name_plural = _('Subscriber')

    name = models.CharField(
        verbose_name=_('name'),
        max_length=255,
        null=False,
        blank=False,
    )

    user = models.CharField(
        verbose_name=_('user'),
        max_length=255,
        null=False,
        blank=False,
    )

    groups = models.ManyToManyField(Group)
    
    def __str__(self):
        return self.name

# Model Device.
class Device(UUIDPkMixin, ActivableMixin, DateTimeManagementMixin, models.Model):
    class Meta:
        verbose_name = _('Device')
        verbose_name_plural = _('Device')

    subscriber = models.ForeignKey(
        Subscriber,
        models.DO_NOTHING,
        db_column='user',
        null=False,
        blank=False,
    )

    name = models.CharField(
        verbose_name=_('name'),
        max_length=255,
        null=False,
        blank=False,
    )

    broker_type = models.CharField(
        verbose_name=_('broker type'),
        max_length=255,
        null=False,
        blank=False,
    )

    broker_id = models.IntegerField(
        verbose_name=_('broker id'),
        db_index=True,
        unique=True,
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
    
    unique_id = models.IntegerField(
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

    os_build_number = models.IntegerField(
        verbose_name=_('os build number'),
        db_index=True,
        unique=True,
        null=False,
        blank=False,
    )

    os_version = models.IntegerField(
        verbose_name=_('os version'),
        db_index=True,
        unique=True,
        null=False,
        blank=False,
    )

    os_bundle_id = models.IntegerField(
        verbose_name=_('os bundle id'),
        db_index=True,
        unique=True,
        null=False,
        blank=False,
    )

    os_readable_version = models.IntegerField(
        verbose_name=_('os readable version'),
        db_index=True,
        unique=True,
        null=False,
        blank=False,
    )

    android_fringerprint = models.CharField(
        verbose_name=_('android fingerprint'),
        max_length=255,
        null=True,
        blank=True,
    )

    android_install_time = models.CharField(
        verbose_name=_('android install time'),
        max_length=255,
        null=True,
        blank=True,
    )

    android_bootloader = models.CharField(
        verbose_name=_('android bootloader'),
        max_length=255,
        null=True,
        blank=True,
    )

    ios_device_token = models.CharField(
        verbose_name=_('ios device token'),
        max_length=255,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name

# Model Notification.
class Notification(UUIDPkMixin, ActivableMixin, DateTimeManagementMixin, models.Model):
    class Meta:
        verbose_name = _('Notification')
        verbose_name_plural = _('Notification')

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

    status = models.CharField(
        verbose_name=_('status'),
        max_length=255,
        choices=constants.STATUS_NOTIFICATION,
        blank=False,
        null=False
    )

    text = models.CharField(
        verbose_name=_('text'),
        max_length=255,
        null=False,
        blank=False,
    )

    device = models.ForeignKey(
        Device,
        models.DO_NOTHING,
        db_column='unique_id',
        null=False,
        blank=False,
    )

    extra_data = jsonfield.JSONField(
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name