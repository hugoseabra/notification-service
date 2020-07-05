import json

from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.test import TestCase
from django.urls import reverse

from apps.notification.models import Notification
from apps.notification.tests import utils


class NotificationAPITest(TestCase):
    """
    Testes de API - CRUD
    """

    fixtures = (
        '000_site_dev',
    )

    def setUp(self):
        self.user, _ = User.objects.get_or_create(
            username='sample-user',
            is_superuser=True,
            is_staff=True,
        )

        self.namespace = utils.create_namespace(save=True)

        notification = utils.create_notification(save=False)
        notification.validate()
        notification.save()

        self.data = {
            'language': notification.language,
            'title': notification.title,
            'text': notification.text,
            'type': notification.type,
        }
        notification.delete()

    def _login(self):
        self.client.force_login(user=self.user)

    def _get_collection_endpoint(self):
        url = reverse('notification-list')
        return f'{url}?namespace={self.namespace.pk}'

    def _get_item_endpoint(self, pk):
        return reverse('notification-detail', kwargs={
            'pk': pk,
        })

    def _get_uri(self, endpoint):
        site = Site.objects.get_current()
        domain = site.domain
        domain = domain.rtrim('/') if str(domain).endswith('/') else domain
        return 'http://{}{}'.format(domain, endpoint)

    def _create_instance(self):
        instance = utils.create_notification(save=False)
        instance.namespace = self.namespace
        instance.validate()
        instance.save()
        return instance

    def test_private_endpoints(self):
        uri = self._get_uri(self._get_collection_endpoint())
        result = self.client.get(
            path=uri,
            content_type='application/json',
        )
        self.assertEqual(result.status_code, 401)

        instance = utils.create_namespace(save=True)
        uri = self._get_uri(self._get_item_endpoint(instance.pk))
        result = self.client.get(
            path=uri,
            content_type='application/json',
        )
        self.assertEqual(result.status_code, 401)

    def test_creation(self):
        uri = self._get_uri(self._get_collection_endpoint())

        self._login()

        self.data.update({'namespace': {
            'pk': str(self.namespace.pk)
        }})

        result = self.client.post(
            path=uri,
            data=json.dumps(self.data),
            content_type='application/json',
        )
        data = result.json()
        self.assertEqual(result.status_code, 201)

        self.assertTrue(Notification.objects.filter(pk=data['pk']))

    def test_creation_with_groups(self):
        uri = self._get_uri(self._get_collection_endpoint())

        self._login()

        self.data.update({'namespace': {
            'pk': str(self.namespace.pk)
        }})

        group1 = utils.create_group(save=False)
        group1.namespace = self.namespace
        group1.save(ignore_validation=True)

        group2 = utils.create_group(save=True, ignore_validation=True)
        group2.namespace = self.namespace
        group2.save(ignore_validation=True)

        self.data['groups'] = [
            {
                'pk': str(group1.pk),
            },
            {
                'pk': str(group2.pk),
            }
        ]

        result = self.client.post(
            path=uri,
            data=json.dumps(self.data),
            content_type='application/json',
        )
        data = result.json()
        self.assertEqual(result.status_code, 201)

        instance = Notification.objects.get(pk=data['pk'])
        self.assertTrue(instance.groups.count() == 2)

        group_pks = [str(g.pk) for g in instance.groups.all()]
        self.assertIn(str(group1.pk), group_pks)
        self.assertIn(str(group2.pk), group_pks)

    def test_edit(self):
        instance = self._create_instance()

        uri = self._get_uri(self._get_item_endpoint(pk=instance.pk))

        self._login()

        result = self.client.patch(
            path=uri,
            data=json.dumps(self.data),
            content_type='application/json',
        )
        print(result.json())
        self.assertEqual(result.status_code, 200)

        instance = Notification.objects.get(pk=instance.pk)

        for k, v in self.data.items():
            instance_value = getattr(instance, k)
            if v == '':
                v = None

            if instance_value == '':
                instance_value = None

            self.assertEqual(v, instance_value)

    def test_edit_groups(self):
        instance = self._create_instance()

        group1 = utils.create_group(save=False)
        group1.namespace = self.namespace
        group1.save(ignore_validation=True)

        group2 = utils.create_group(save=True, ignore_validation=True)
        group2.namespace = self.namespace
        group2.save(ignore_validation=True)

        self.assertTrue(instance.groups.count() == 0)

        data = {'groups': [
            {'pk': str(group1.pk)},
            {'pk': str(group2.pk)},
        ]}

        uri = self._get_uri(self._get_item_endpoint(pk=instance.pk))

        self._login()

        result = self.client.patch(
            path=uri,
            data=json.dumps(data),
            content_type='application/json',
        )
        print(result.json())
        self.assertEqual(result.status_code, 200)

        instance = Notification.objects.get(pk=instance.pk)

        self.assertTrue(instance.groups.count() == 2)

        group_pks = [str(g.pk) for g in instance.groups.all()]
        self.assertIn(str(group1.pk), group_pks)
        self.assertIn(str(group2.pk), group_pks)

        group3 = utils.create_group(save=True, ignore_validation=True)
        group3.namespace = self.namespace
        group3.save(ignore_validation=True)

        data = {'groups': [
            {'pk': str(group1.pk)},
            {'pk': str(group3.pk)},
        ]}

        uri = self._get_uri(self._get_item_endpoint(pk=instance.pk))

        self._login()

        result = self.client.patch(
            path=uri,
            data=json.dumps(data),
            content_type='application/json',
        )
        print(result.json())
        self.assertEqual(result.status_code, 200)

        instance = Notification.objects.get(pk=instance.pk)

        group_pks = [str(g.pk) for g in instance.groups.all()]
        self.assertIn(str(group1.pk), group_pks)
        self.assertNotIn(str(group2.pk), group_pks)
        self.assertIn(str(group3.pk), group_pks)

    def test_delete(self):
        instance = self._create_instance()
        uri = self._get_uri(self._get_item_endpoint(pk=instance.pk))

        self._login()

        result = self.client.delete(
            path=uri,
            data=json.dumps(self.data),
            content_type='application/json',
        )
        self.assertEqual(result.status_code, 204)

        # noinspection PyTypeChecker
        with self.assertRaises(Notification.DoesNotExist):
            Notification.objects.get(pk=instance.pk)
