from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.notification.models import Notification
from apps.notification import services


@receiver(post_save, sender=Notification)
def create_transmissions(instance, **_):
    services.create_transmissions(notification=instance)
