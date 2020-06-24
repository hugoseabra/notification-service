from django.utils.translation import gettext_lazy as _

STATUS_NOTIFICATION = (
    ("waiting", _("Waiting")),
    ("delivered", _("Delivered")),
    ("retry", _("Retry")),
    ("failed", _("Failed")),
    ("cancelled", _("Cancelled")),
)