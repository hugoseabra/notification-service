import importlib
from typing import List

from django.db.models import QuerySet

from apps.notification.models import Notification, Transmission, Namespace
from brokers import Broker, value_objects
from .constants import BROTKER_TYPES
from .forms import TransmissionForm


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


def create_transmissions(notification: Notification) -> List[Transmission]:
    """
    Creates transmissions for every Subscriber's active device.
    """
    devices = list()
    for subscriber in notification.namespace.subscribers.filter(active=True):
        devices += [d for d in subscriber.devices.filter(active=True)]

    for device in devices:
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

    broker = get_broker(
        broker_alias=namespace.broker_type,
        api_key=namespace.broker_api_key,
        app_id=namespace.broker_app_id
    )

    broker_notifications = list()

    for sub in namespace.subscribers.filter(active=True):
        notifications = dict()

        for notif in sub.notifications.filter(broker_id__isnull=True):
            broker_notification = value_objects.Notification(
                url=url,
                app_id=namespace.broker_app_id,
            )
            print(broker_notification)

            transmissions = notif.transmissions.filter(
                processed_at__isnull=True
            )
            notifications[str(notif.pk)] = notif

            device_broker_ids = list()

            for transmission in transmissions:
                subscriber = transmission.notification.subscriber
                notification = transmission.notification

                device_broker_ids += [
                    d.broker_id
                    for d in subscriber.devices.filter(active=True)
                    if d.broker_id
                ]

                broker_notification.add_heading(
                    language=notification.language,
                    plain_text=notification.title,
                )
                broker_notification.add_content(
                    language=notification.language,
                    plain_text=notification.text,
                )

            for broker_id in device_broker_ids:
                broker_notification.add_player_id(player_id=broker_id)

            broker_notifications.append(broker_notification)

    print(broker_notifications)

    # for broker_notif in broker_notifications:
    #     response = broker.create_and_send_notification(data=dict(broker_notif))
    #
    #     if response.status_code != 200:
    #         raise Exception(
    #             f'Error when synchronizing notifications'
    #             f' - Status: {response.status_code}: {response.text}'
    #         )
    #
    #     data = response.json()
    #
    #     for _, notification in notifications.items():
    #         id = data.get('id')
    #         if notification.broker_id is not None:
    #             continue
    #         if id:
    #             notification.broker_id = id
    #             notification.validate()
    #             notification.save()
