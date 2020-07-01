from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.notification.tests import utils


class DeviceAndNotificationSameSubscriberTest(TestCase):
    """
    Tests of main relations of a transmission (device and notification)
    checking them if they reference the same Subscriber.
    """

    def setUp(self):
        self.instance = utils.create_transmission(save=False)

    def test_error_device_notification_diff_subscriber(self):
        """
        Test adding a device and a notification into a Tranmission with
        different Subscriber related.
        """
        notification = utils.create_notification(save=True,
                                                 ignore_validation=True)
        self.instance.notification = notification

        with self.assertRaises(ValidationError) as e:
            self.instance.validate()

        message = str(e.exception.message)
        self.assertIn('TRANSMISSION01', message)

    def test_ok_device_notification_same_subscriber(self):
        """
        Test adding a device and a notification into a Tranmission with
        same Subscriber related.
        """
        notification = utils.create_notification(save=True,
                                                 ignore_validation=True)
        device = utils.create_device(save=False)
        device.subscriber = notification.subscriber
        device.save(ignore_validation=True)

        self.instance.device = device
        self.instance.notification = notification

        self.instance.validate()
        self.instance.save()
