from django.utils.translation import gettext_lazy as _

BROKER_TYPE_ONESIGNAL = 'onesignal'

BROTKER_TYPES = (
    (BROKER_TYPE_ONESIGNAL, _("OneSignal")),
)

NOTIFICATION_LANG_EN = 'en'
NOTIFICATION_LANG_PT = 'pt'
NOTIFICATION_LANGUAGES = (
    (NOTIFICATION_LANG_EN, 'English'),
    (NOTIFICATION_LANG_PT, 'Portuguese'),
)

TRANSMISSION_STATUS_WAITING = 'waiting'
TRANSMISSION_STATUS_DELIVERED = 'delivered'
TRANSMISSION_STATUS_RETRY = 'retry'
TRANSMISSION_STATUS_FAILED = 'failed'
TRANSMISSION_STATUS_CANCELLED = 'cancalled'

TRANSMISSION_STATUSES = (
    (TRANSMISSION_STATUS_WAITING, _("Waiting")),
    (TRANSMISSION_STATUS_DELIVERED, _("Delivered")),
    (TRANSMISSION_STATUS_RETRY, _("Retry")),
    (TRANSMISSION_STATUS_FAILED, _("Failed")),
    (TRANSMISSION_STATUS_CANCELLED, _("Cancelled")),
)
