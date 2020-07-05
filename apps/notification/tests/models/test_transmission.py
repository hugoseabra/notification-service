from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.notification.tests import utils


class DeviceAndNotificationSameNamespaceTest(TestCase):
    """
    Tests of main relations of a transmission (device and notification)
    checking them if they reference the same Subscriber.
    """

    def setUp(self):
        self.instance = utils.create_transmission(save=False)

    def test_error_device_notification_diff_namespace(self):
        """
        Test adding a device and a notification into a Tranmission with
        different Namespaces related.
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
        same Namespace related.
        """
        device = utils.create_device(save=True, ignore_validation=True)

        notification = utils.create_notification(save=False)
        notification.namespace = device.subscriber.namespace
        notification.save(ignore_validation=True)

        self.instance.device = device
        self.instance.notification = notification

        self.instance.validate()
        self.instance.save()


class TransmissionCreationByNotificationCreationTest(TestCase):
    """
    Tests checks if transmission are created by Notification signal when a
    notification is created.
    """

    def setUp(self):
        self.namespace = utils.create_namespace(save=True,
                                                ignore_validation=True)

    def _prepare_data(self):
        """
        3 groups and 7 devices
        """
        self.group1 = utils.create_group(save=False)
        self.group1.namespace = self.namespace
        self.group1.save(ignore_validation=True)

        self.group2 = utils.create_group(save=False)
        self.group2.namespace = self.namespace
        self.group2.save(ignore_validation=True)

        # 3 devices into group1
        self.device1 = self._create_device()
        self.device2 = self._create_device()
        self.device3 = self._create_device()

        self.device1.subscriber.groups.add(self.group1)
        self.device2.subscriber.groups.add(self.group1)
        self.device3.subscriber.groups.add(self.group1)

        # 2 devices into group2
        self.device4 = self._create_device()
        self.device5 = self._create_device()

        self.device4.subscriber.groups.add(self.group2)
        self.device5.subscriber.groups.add(self.group2)

        # 2 devices into group1 and group2
        self.device6 = self._create_device()
        self.device7 = self._create_device()

        self.device6.subscriber.groups.add(self.group1)
        self.device6.subscriber.groups.add(self.group2)

        self.device7.subscriber.groups.add(self.group1)
        self.device7.subscriber.groups.add(self.group2)

        # NOW we have 2 groups and 7 devices

    def _create_device(self):
        subscriber1 = utils.create_subscriber(save=False)
        subscriber1.namespace = self.namespace
        subscriber1.save(ignore_validation=True)

        # Adds 1 device to subscriber
        device = utils.create_device(save=False)
        device.subscriber = subscriber1
        device.save(ignore_validation=True)

        return device

    def test_transmissions_for_all_subscribers(self):
        """
        Tests creation of transmissions by signals just after creating
        notifications.
        """
        device1 = self._create_device()
        device2 = self._create_device()

        # Add notification
        notification = utils.create_notification(save=False)
        notification.namespace = self.namespace
        notification.validate()
        notification.save()

        notification.process_transmissions()

        # As soon a notification is saved with the same namespace of the
        # 2 previous subscribers, SIGNALS musts create Transmissions for each
        # one of them
        self.assertEqual(notification.transmissions.count(), 2)

        devices_pks = [
            str(t.device_id)
            for t in notification.transmissions.all()
        ]

        self.assertIn(str(device1.pk), devices_pks)
        self.assertIn(str(device2.pk), devices_pks)

    def test_transmissions_for_defined_groups(self):
        """
        Tests creation of transmissions by signals just after creating
        notifications.
        """
        self._prepare_data()

        # Add notification
        notification = utils.create_notification(save=False)
        notification.namespace = self.namespace
        notification.validate()
        notification.save()

        # Let's add group1 and group2 into notification
        notification.groups.add(self.group1)
        notification.groups.add(self.group2)

        # Group1: 5 devices according to prepare data
        all_devices = list()
        devices = 0
        for subscriber in self.group1.subscribers.all():
            all_devices += [d for d in subscriber.devices.all()]
            devices += subscriber.devices.count()

        self.assertEqual(devices, 5)

        # Group2: 4 devices according to prepare data
        devices = 0
        for subscriber in self.group2.subscribers.all():
            all_devices += [d for d in subscriber.devices.all()]
            devices += subscriber.devices.count()

        self.assertEqual(devices, 4)

        # However, 2 subscribers are related to 2 groups. So, the total of
        # subscribers involved are 9 - 2 = 7
        # IN THE TEST CASE, WE HAVE 1 DEVICE PER SUBSCRIBER
        self.assertEqual(self.namespace.subscribers.count(), 7)

        # 5 + 4 devices = 9 devices = 9 transmissions
        notification.process_transmissions()

        self.assertEqual(notification.transmissions.count(), 7)
