from apps.notification.models import Notification, Transmission


def get_broker():
    pass


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
