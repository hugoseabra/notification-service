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
    for device in notification.subscriber.devices.filter(active=True):
        filters = {
            'notification_id': str(notification.pk),
            'device_id': str(device.pk),
        }

        if Transmission.objects.filter(**filters).exists() is False:
            transmission = Transmission(
                device_id=str(device.pk),
                notification_id=str(notification.pk),
            )
            transmission.validate()
            transmission.save()


def send_notifications(namespace: Namespace):
    """
    Processes transmissions by sending notification to Push Notification broker.
    """
    url = 'clientize://'

    broker_notification = value_objects.Notification(
        url=url,
        app_id=namespace.broker_app_id,
    )

    transmissions = Transmission.objects.filter(
        notification__subscriber__namespace_id=namespace.pk,
        processed_at__isnull=True
    )

    broker = get_broker(
        broker_alias=namespace.broker_type,
        api_key=namespace.broker_api_key,
        app_id=namespace.broker_app_id
    )

    notifications = list()

    device_broker_ids = list()

    for transmission in transmissions:
        subscriber = transmission.notification.subscriber
        device_broker_ids += [
            d.broker_id
            for d in subscriber.devices.filter(active=True)
            if d.broker_id
        ]
        notifications.append(transmission.notification)

    for id in device_broker_ids:
        broker_notification.add_player_id(player_id=id)

    response = broker.create_and_send_notification(
        data=dict(broker_notification)
    )

    if response.status_code != 200:
        raise Exception(
            f'Error when synchronizing notifications'
            f' - Status: {response.status_code}: {response.text}'
        )

    data = response.json()

    for notification in notifications:
        id = data.get('id')
        if notification.broker_id is not None:
            continue
        if id:
            notification.broker_id = id
            notification.validate()
            notification.save()
