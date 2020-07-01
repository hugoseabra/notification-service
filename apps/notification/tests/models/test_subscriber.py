from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.notification.tests import utils


class GroupWithSameNamespaceTest(TestCase):
    """
    Tests preserves relation between subscribers and groups with the same
    namespace.
    """

    def setUp(self):
        self.instance = utils.create_subscriber(save=False)

    def test_ok_when_no_groups(self):
        """
        Tests success when a subscriber is created with no group related.
        """
        self.assertEqual(self.instance.groups.count(), 0)

        self.instance.validate()
        self.instance.save()

    def test_error_add_group_diff_namespace(self):
        """
        Test adding group with a different namespace from the subscriber's
        namespace.
        """
        group = utils.create_group(save=True, ignore_validation=True)

        # Create subscriber due to n-n relation which has to exists in
        # in persistence before adding group into it.
        self.instance.validate()
        self.instance.save()

        # Group has different namespace from subscriber instance
        with self.assertRaises(Exception):
            self.instance.groups.add(group)

    def test_success_group_same_namespace(self):
        """
        Test adding group with the same namespace from the subscriber's
        namespace.
        """
        group = utils.create_group(save=True)
        group.namespace = self.instance.namespace
        group.save(ignore_validation=True)

        group2 = utils.create_group(save=True)
        group2.namespace = self.instance.namespace
        group2.save(ignore_validation=True)

        self.instance.groups.add(group)
        self.instance.groups.add(group2)

        self.instance.validate()
        self.instance.save()
