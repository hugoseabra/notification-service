import json

from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.test import TestCase
from django.urls import reverse

from apps.notification.models import Device
from apps.notification.tests import utils


class DeviceAPITest(TestCase):
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

        self.subscriber = utils.create_subscriber(save=True,
                                                  ignore_validation=True)

        instance = utils.create_device(save=False)
        instance.validate()
        instance.save()

        self.data = {
            'name': instance.name,
            'broker_id': instance.broker_id,
            'device_type': instance.device_type,
            'model': instance.model,
            'unique_id': instance.unique_id,
            'brand': instance.brand,
            'os_build_number': instance.os_build_number,
            'os_version': instance.os_version,
            'os_bundle_id': instance.os_bundle_id,
            'os_readable_version': instance.os_readable_version,
            'android_fingerprint': instance.android_fingerprint,
            'android_install_time': instance.android_install_time,
            'android_bootloader': instance.android_bootloader,
            'ios_device_token': instance.ios_device_token,
        }
        instance.delete()

    def _login(self):
        self.client.force_login(user=self.user)

    def _get_collection_endpoint(self):
        uri = reverse('device-list')
        return f'{uri}?subscriber={self.subscriber.pk}'

    def _get_item_endpoint(self, pk):
        return reverse('device-detail', kwargs={'pk': pk})

    def _get_uri(self, endpoint):
        site = Site.objects.get_current()
        domain = site.domain
        domain = domain.rtrim('/') if str(domain).endswith('/') else domain
        return 'http://{}{}'.format(domain, endpoint)

    def _create_instance(self):
        instance = utils.create_device(save=False)
        instance.subscriber = self.subscriber
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

        self.data.update({'subscriber': {
            'pk': str(self.subscriber.pk)
        }})

        result = self.client.post(
            path=uri,
            data=json.dumps(self.data),
            content_type='application/json',
        )

        data = result.json()
        self.assertEqual(result.status_code, 201)

        self.assertTrue(Device.objects.filter(pk=data['pk']))

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

        instance = Device.objects.get(pk=instance.pk)

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
        with self.assertRaises(Device.DoesNotExist):
            Device.objects.get(pk=instance.pk)
