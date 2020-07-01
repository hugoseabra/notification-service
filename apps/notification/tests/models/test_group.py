from django.test import TestCase

from apps.notification.tests import utils


class SubscriberWithSameNamespaceTest(TestCase):
    """
    Tests preserves relation between subscribers and groups with the same
    namespace.
    """

    def setUp(self):
        self.instance = utils.create_group(save=False)

    def test_ok_when_no_subscribers(self):
        """
        Tests success when a group is created with no group related.
        """
        self.assertEqual(self.instance.subscribers.count(), 0)

        self.instance.validate()
        self.instance.save()

    def test_error_add_subscriber_diff_namespace(self):
        """
        Test adding group with a different namespace from the subscriber's
        namespace.
        """
        subscriber = utils.create_subscriber(save=True, ignore_validation=True)

        # Create group due to n-n relation which has to exists in
        # in persistence before adding group into it.
        self.instance.validate()
        self.instance.save()

        # Group has different namespace from subscriber instance
        with self.assertRaises(Exception):
            self.instance.subscribers.add(subscriber)

    def test_success_subscriber_same_namespace(self):
        """
        Test adding group with the same namespace from the subscriber's
        namespace.
        """
        subscriber = utils.create_subscriber(save=True)
        subscriber.namespace = self.instance.namespace
        subscriber.save(ignore_validation=True)

        subscriber2 = utils.create_subscriber(save=True)
        subscriber2.namespace = self.instance.namespace
        subscriber2.save(ignore_validation=True)

        self.instance.subscribers.add(subscriber)
        self.instance.subscribers.add(subscriber2)

        self.instance.validate()
        self.instance.save()
