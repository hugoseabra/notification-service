import uuid
from django.test import TestCase

from apps.notification.forms import SubscriberForm
from apps.notification.tests import utils


class SubscriberFormTest(TestCase):
    """
    Form Tests
    """
    def setUp(self):
        self.namespace = utils.create_namespace(save=True,
                                                ignore_validation=True)
        self.data = {
            'user_id': uuid.uuid4(),
            'name': 'Luke Skywalker',
            'user': '0c1c921b-374a-4ede-954e-a5f835a15e9b',
            'namespace': str(self.namespace.pk)
        }

    def create_form(self, **kwargs) -> SubscriberForm:
        return SubscriberForm(**kwargs)

    def test_ok_create_subscriber_with_no_groups(self):
        """
        Tests creation of a subscriber with no groups.
        """
        form = self.create_form(data=self.data)
        self.assertTrue(form.is_valid())
        form.save()

    def test_error_new_subscriber_with_group_diff_namespace(self):
        """
        Tests add groups to a subscriber with different namespace.
        """
        # Groups with different namespace from Subscriber in Form
        group = utils.create_group(save=True, ignore_validation=True)
        group2 = utils.create_group(save=True, ignore_validation=True)

        self.data['groups'] = [group, group2]

        form = self.create_form(data=self.data)

        self.assertFalse(form.is_valid())

    def test_error_edit_subscriber_with_group_diff_namespace(self):
        """
        Tests add groups to a subscriber with different namespace.
        """
        # Groups with different namespace from Subscriber in Form
        group = utils.create_group(save=True, ignore_validation=True)
        group2 = utils.create_group(save=True, ignore_validation=True)

        subscriber = utils.create_subscriber(save=True, ignore_validation=True)

        self.data['groups'] = [group, group2]

        form = self.create_form(data=self.data, instance=subscriber)

        self.assertFalse(form.is_valid())

    def test_ok_add_subscriber_with_groups_same_namespace(self):
        """
        Tests adding a subscriber with groups with the same namespace.
        """
        # Groups with different namespace from Subscriber in Form
        group = utils.create_group(save=False)
        group.namespace = self.namespace
        group.save(ignore_validation=True)

        group2 = utils.create_group(save=False)
        group2.namespace = self.namespace
        group2.save(ignore_validation=True)

        self.data['groups'] = [group, group2]

        form = self.create_form(data=self.data)

        self.assertTrue(form.is_valid())
        form.save()

        group_pks = [str(g.pk) for g in form.instance.groups.all()]

        self.assertIn(str(group.pk), group_pks)
        self.assertIn(str(group2.pk), group_pks)

    def test_ok_edit_subscriber_with_groups_same_namespace(self):
        """
        Tests editing a subscriber with groups with the same namespace.
        """
        # Groups with different namespace from Subscriber in Form
        group = utils.create_group(save=False)
        group.namespace = self.namespace
        group.save(ignore_validation=True)

        group2 = utils.create_group(save=False)
        group2.namespace = self.namespace
        group2.save(ignore_validation=True)

        subscriber = utils.create_subscriber(save=True, ignore_validation=True)

        self.assertEqual(subscriber.groups.count(), 0)

        self.data['groups'] = [group, group2]

        form = self.create_form(data=self.data, instance=subscriber)

        self.assertTrue(form.is_valid())
        form.save()

        group_pks = [str(g.pk) for g in subscriber.groups.all()]

        self.assertIn(str(group.pk), group_pks)
        self.assertIn(str(group2.pk), group_pks)
