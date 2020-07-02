import importlib

from django.db.models import QuerySet

from apps.notification.models import Notification, Transmission, Namespace
from brokers import Broker, value_objects
from .constants import BROTKER_TYPES


def get_broker(broker_alias, **kwargs) -> Broker:
    brokers = list()
    for item in BROTKER_TYPES:
        brokers.append(item[0])

    if broker_alias not in brokers:
        raise Exception(f'Invalid broker: {broker_alias}')

    module = importlib.import_module(f'brokers.{broker_alias}')
    broker_client_class = module.Client
    return broker_client_class(**kwargs)


def process_notifications(queryset: QuerySet = None):
    """
    Swap notifications to check if all transmissions are created.
    """
    if queryset is None:
        queryset = Notification.objects.all()

    for notification in queryset:
        create_transmissions(notification)


def create_transmissions(notification: Notification):
    """
    Creates transmissions for every Subscriber's active device.
    """
    pass


def send_notification(transmission: Transmission):
    """
    Processes transmission by sending notification to Push Notification
    broker.
    """
    pass
