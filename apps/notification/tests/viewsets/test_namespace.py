import json

from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.test import TestCase
from django.urls import reverse

from apps.notification.models import Namespace
from apps.notification.tests import utils


class NamespaceAPITest(TestCase):
    """
    Testes de API - CRUD
    """

    fixtures = (
        '000_site_dev',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def setUp(self):
        self.user, _ = User.objects.get_or_create(
            username='sample-user',
            is_superuser=True,
            is_staff=True,
        )

        namespace = utils.create_namespace(save=True)
        self.data = {
            'name': namespace.name,
            'external_id': namespace.external_id,
            'description': namespace.description,
            'broker_type': namespace.broker_type,
            'broker_app_id': namespace.broker_app_id,
            'broker_api_key': namespace.broker_api_key,
        }
        namespace.delete()

    def _login(self):
        self.client.force_login(user=self.user)

    def _get_collection_endpoint(self):
        return reverse('namespace-list')

    def _get_item_endpoint(self, pk):
        return reverse('namespace-detail', kwargs={'pk': pk})

    def _get_uri(self, endpoint):
        site = Site.objects.get_current()
        domain = site.domain
        domain = domain.rtrim('/') if str(domain).endswith('/') else domain
        return 'http://{}{}'.format(domain, endpoint)

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

    def test_admin_endpoints(self):
        # Forces user as not admin
        self.user.is_staff = False
        self.user.is_superuser = False
        self.user.save()

        self._login()

        uri = self._get_uri(self._get_collection_endpoint())
        result = self.client.get(
            path=uri,
            content_type='application/json',
        )
        self.assertEqual(result.status_code, 403)

        instance = utils.create_namespace(save=True)
        uri = self._get_uri(self._get_item_endpoint(instance.pk))
        result = self.client.get(
            path=uri,
            content_type='application/json',
        )
        self.assertEqual(result.status_code, 403)

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

        self.assertTrue(Namespace.objects.filter(pk=data['pk']))

    def test_edit(self):
        namespace = utils.create_namespace(save=True)
        uri = self._get_uri(self._get_item_endpoint(pk=namespace.pk))

        self._login()

        result = self.client.patch(
            path=uri,
            data=json.dumps(self.data),
            content_type='application/json',
        )
        self.assertEqual(result.status_code, 200)

        namespace = Namespace.objects.get(pk=namespace.pk)

        for k, v in self.data.items():
            instance_value = getattr(namespace, k)
            if v == '':
                v = None

            if instance_value == '':
                instance_value = None

            self.assertEqual(v, instance_value)

    def test_delete(self):
        namespace = utils.create_namespace(save=True)
        uri = self._get_uri(self._get_item_endpoint(pk=namespace.pk))

        self._login()

        result = self.client.delete(
            path=uri,
            data=json.dumps(self.data),
            content_type='application/json',
        )
        self.assertEqual(result.status_code, 204)

        # noinspection PyTypeChecker
        with self.assertRaises(Namespace.DoesNotExist):
            Namespace.objects.get(pk=namespace.pk)
