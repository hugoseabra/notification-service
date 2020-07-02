from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.notification.models import Notification
from apps.notification.services import create_transmissions as service


@receiver(post_save, sender=Notification)
def create_transmissions(instance, **_):
    service(notification=instance)
