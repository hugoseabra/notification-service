import importlib
from typing import List

from django.db.models import QuerySet, Q
from django.db.transaction import atomic
from django.utils import timezone

from apps.notification.models import (
    Device,
    Namespace,
    Notification,
    Transmission,
    Subscriber,
)
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

            yield transmission


def process_namespaces_notifications():
    for n in Namespace.objects.filter(active=True):
        send_notifications(namespace=n)


def send_notifications(namespace: Namespace):
    """
    Processes transmissions by sending notification to Push Notification broker.
    """
    url = 'clientize://'

    msg = f'Processing namespace: {namespace}'
    print('=' * len(msg))
    print(msg)
    print('=' * len(msg))

    broker = get_broker(
        broker_alias=namespace.broker_type,
        api_key=namespace.broker_api_key,
        app_id=namespace.broker_app_id
    )

    notifi_qs = namespace.notifications.filter(
        Q(broker_id='')|Q(broker_id__isnull=True)
    )

    print(f'= Broker: {namespace.broker_type}')
    print(f'= # Notifications: {notifi_qs.count()}')

    if namespace.last_process is not None:
        print(f'= Last process: {timezone.localtime(namespace.last_process)}')
        notifi_qs = notifi_qs.filter(created_at__gte=namespace.last_process)

    broker_notifications = list()

    for notif in notifi_qs:
        print()
        print(f' > Notification: {notif.title} ({notif.pk})')

        broker_notification = value_objects.Notification(
            url=url,
            app_id=namespace.broker_app_id,
        )
        broker_notification.django_notification_id = str(notif.pk)

        broker_notification.add_heading(
            language=notif.language,
            plain_text=notif.title,
        )

        broker_notification.add_content(
            language=notif.language,
            plain_text=notif.text,
        )

        subscriber_qs = Subscriber.objects.filter(
            active=True,
            devices__broker_id__isnull=False,
            devices__active=True,
        )

        group_qs = notif.groups.filter(active=True)

        print(f'   - Groups: {group_qs.count()}')

        if group_qs.count():
            groups_pk = [str(g.pk) for g in group_qs]
            subscriber_qs = subscriber_qs.filter(groups__pk__in=groups_pk)

        print(f'   - Subscribers: {subscriber_qs.count()}')
        subscriber_pks = [str(s.pk) for s in subscriber_qs]

        device_qs = Device.objects.filter(
            broker_id__isnull=False,
            active=True,
            subscriber_id__in=subscriber_pks,
        )

        print(f'   - devices: {device_qs.count()}')

        for d in device_qs:
            broker_notification.add_player_id(player_id=d.broker_id)

        broker_notifications.append(broker_notification)

    with atomic():
        for broker_notif in broker_notifications:
            response = broker.create_and_send_notification(
                data=dict(broker_notif))

            if response.status_code != 200:
                raise Exception(
                    f'Error when synchronizing notifications'
                    f' - Status: {response.status_code}: {response.text}'
                )

            data = response.json()

            notif = Notification.objects.get(
                pk=broker_notif.django_notification_id
            )
            notif.broker_id = data.get('id')
            notif.validate()
            notif.save()

            namespace.last_process = timezone.now()
            namespace.validate()
            namespace.save()

    print()
