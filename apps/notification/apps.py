from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class NotificationConfig(AppConfig):
    name = 'apps.notification'
    label = 'notification'
    verbose_name = _('Notification')

    # noinspection PyUnresolvedReferences
    def ready(self):
        import apps.notification.signals
