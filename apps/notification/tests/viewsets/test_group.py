import json

from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.test import TestCase
from django.urls import reverse

from apps.notification.models import Group
from apps.notification.tests import utils


class GroupAPITest(TestCase):
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

        group = utils.create_group(save=False)
        group.validate()
        group.save()

        self.data = {
            'name': group.name,
            'alias': group.alias,
        }
        group.delete()

    def _login(self):
        self.client.force_login(user=self.user)

    def _get_collection_endpoint(self):
        return reverse('group-list',
                       kwargs={'namespace_pk': self.namespace.pk})

    def _get_item_endpoint(self, pk):
        return reverse('group-detail', kwargs={
            'pk': pk,
            'namespace_pk': self.namespace.pk,
        })

    def _get_uri(self, endpoint):
        site = Site.objects.get_current()
        domain = site.domain
        domain = domain.rtrim('/') if str(domain).endswith('/') else domain
        return 'http://{}{}'.format(domain, endpoint)

    def _create_instance(self):
        instance = utils.create_group(save=False)
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

        result = self.client.post(
            path=uri,
            data=json.dumps(self.data),
            content_type='application/json',
        )

        data = result.json()
        self.assertEqual(result.status_code, 201)

        self.assertTrue(Group.objects.filter(pk=data['pk']))

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

        instance = Group.objects.get(pk=instance.pk)

        for k, v in self.data.items():
            instance_value = getattr(instance, k)
            if v == '':
                v = None

            if instance_value == '':
                instance_value = None

            self.assertEqual(v, instance_value)

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
        with self.assertRaises(Group.DoesNotExist):
            Group.objects.get(pk=instance.pk)
