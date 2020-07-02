import uuid

from django.test import TestCase

from apps.notification.models import Subscriber
from apps.notification.serializers import SubscriberSerializer, GroupSerializer
from apps.notification.tests import utils


class SubscriberSerializerTest(TestCase):
    """
    Serializer Tests
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

    def create_serializer(self, **kwargs) -> SubscriberSerializer:
        return SubscriberSerializer(**kwargs)

    def test_ok_output_contains_groups_key(self):
        """
        Tests serializer outputs a schema container "groups" key as array
        """
        serializer = self.create_serializer(data=self.data)
        serializer.is_valid()

        data = serializer.validated_data
        self.assertIn('groups', data.keys())

    def test_ok_output_contains_groups_data(self):
        """
        Tests serializer outputs lists groups as Group's serializers output
        in array items.
        """
        subscriber = utils.create_subscriber(save=True, ignore_validation=True)

        group = utils.create_group(save=True, ignore_validation=True)
        group2 = utils.create_group(save=True, ignore_validation=True)

        group.namespace = subscriber.namespace
        group.save(ignore_validation=True)

        group2.namespace = subscriber.namespace
        group2.save(ignore_validation=True)

        subscriber.groups.add(group)
        subscriber.groups.add(group2)

        serializer = self.create_serializer(data=self.data,
                                            instance=subscriber)
        serializer.is_valid(raise_exception=True)
        subscriber_data = serializer.data

        group_serializer = GroupSerializer(instance=group)
        group_keys = group_serializer.data.keys()

        for group_key in group_keys:
            for group_data in subscriber_data['groups']:
                self.assertIn(group_key, group_data)

    def test_ok_input_adding_groups_to_subscriber(self):
        """
        Tests creating a Subscriber with groups added to it.
        """
        data = self.data.copy()

        group = utils.create_group(save=True, ignore_validation=True)
        group.namespace = self.namespace
        group.save(ignore_validation=True)
        group_serializer = GroupSerializer(instance=group)

        group2 = utils.create_group(save=True, ignore_validation=True)
        group2.namespace = self.namespace
        group2.save(ignore_validation=True)
        group_serializer2 = GroupSerializer(instance=group2)

        data['groups'] = [
            group_serializer.data,
            group_serializer2.data,
        ]

        serializer = self.create_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        subscriber = serializer.save()

        sub_group_pks = [str(g.pk) for g in subscriber.groups.all()]

        self.assertIn(str(group.pk), sub_group_pks)
        self.assertIn(str(group2.pk), sub_group_pks)

    def test_ok_input_adding_groups_to_subscriber_by_list_id(self):
        """
        Tests creating a Subscriber with groups added to it.
        """
        data = self.data.copy()

        group = utils.create_group(save=True, ignore_validation=True)
        group.namespace = self.namespace
        group.save(ignore_validation=True)

        group2 = utils.create_group(save=True, ignore_validation=True)
        group2.namespace = self.namespace
        group2.save(ignore_validation=True)

        data['groups'] = [str(group.pk), str(group2.pk)]

        serializer = self.create_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        subscriber = serializer.save()

        sub_group_pks = [str(g.pk) for g in subscriber.groups.all()]

        self.assertIn(str(group.pk), sub_group_pks)
        self.assertIn(str(group2.pk), sub_group_pks)

    def test_ok_input_adding_removing_group_from_subscriber(self):
        """
        Tests editing a Subsbcriber before with 3 groups and now with 2.
        """
        orig_subscriber = utils.create_subscriber(save=False)
        orig_subscriber.namespace = self.namespace
        orig_subscriber.save(ignore_validation=True)

        group = utils.create_group(save=False)
        group.namespace = self.namespace
        group.save(ignore_validation=True)

        group2 = utils.create_group(save=False)
        group2.namespace = self.namespace
        group2.save(ignore_validation=True)

        group3 = utils.create_group(save=False)
        group3.namespace = self.namespace
        group3.save(ignore_validation=True)

        group4 = utils.create_group(save=False)
        group4.namespace = self.namespace
        group4.save(ignore_validation=True)

        orig_subscriber.groups.add(group)
        orig_subscriber.groups.add(group2)
        orig_subscriber.groups.add(group3)
        orig_subscriber.groups.add(group4)

        self.assertEqual(orig_subscriber.groups.count(), 4)

        data = self.data.copy()

        data['groups'] = [str(group.pk), str(group3.pk)]

        serializer = self.create_serializer(data=data,
                                            instance=orig_subscriber)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        subscriber = Subscriber.objects.get(pk=orig_subscriber.pk)
        self.assertEqual(subscriber.groups.count(), 2)

        sub_group_pks = [str(g.pk) for g in subscriber.groups.all()]

        self.assertIn(str(group.pk), sub_group_pks)
        self.assertIn(str(group3.pk), sub_group_pks)

        self.assertNotIn(str(group2.pk), sub_group_pks)
        self.assertNotIn(str(group4.pk), sub_group_pks)
