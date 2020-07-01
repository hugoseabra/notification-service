from django.utils.translation import ugettext_lazy as _

from core.models.mixins import IntegrityRuleChecker, RuleIntegrityError


class DeviceAndNotificationSameSubscriberRule(IntegrityRuleChecker):
    """
    Device and Notification must belong to the same Subscriber
    """

    def check(self, instance):
        """
        :type instance: notification.Transmission
        """
        device_sub_pk = str(instance.device.subscriber_id)
        notif_sub_pk = str(instance.notification.subscriber_id)

        if device_sub_pk != notif_sub_pk:
            raise RuleIntegrityError(
                _(f'Error TRANSMISSION01:'
                  f' Device "{instance.device_id}" and Notification'
                  f' "{instance.notification_id}" are not from the same'
                  f' Subscriber.')
            )
