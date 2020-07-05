from django.utils.translation import ugettext_lazy as _

from core.models.mixins import IntegrityRuleChecker, RuleIntegrityError


class DeviceAndNotificationSameNamespaceRule(IntegrityRuleChecker):
    """
    Device and Notification must belong to the same Namespace
    """

    def check(self, instance):
        """
        :type instance: notification.Transmission
        """
        device_namespace_pk = str(instance.device.subscriber.namespace_id)
        notif_namespace_pk = str(instance.notification.namespace_id)

        if device_namespace_pk != notif_namespace_pk:
            raise RuleIntegrityError(
                _(f'Error TRANSMISSION01:'
                  f' Device "{instance.device_id}" and Notification'
                  f' "{instance.notification_id}" are not from the same'
                  f' Namespace.')
            )
