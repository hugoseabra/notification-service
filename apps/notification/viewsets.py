from rest_framework import status, permissions

from rest_framework.response import Response

from rest_framework.serializers import ListSerializer

from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from core.util.uuid import get_validated_uuid_from_string

from core.viewsets import FieldRequestViewsetMixin

from . import serializers

from django.utils.translation import gettext_lazy as _

from .models import Namespace




class NamespaceViewSet(ModelViewSet):
    serializer_class = serializers.NamespaceSerializer
    queryset = \
        serializers.NamespaceSerializer.Meta.model.objects.get_queryset()

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class GroupViewSet(FieldRequestViewsetMixin, ModelViewSet):
    serializer_class = serializers.GroupSerializer
    queryset = serializers.GroupSerializer.Meta.model.objects.get_queryset()

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_serializer(self, *args, **kwargs):
        serializer = super().get_serializer(*args, **kwargs)

        if isinstance(serializer, ListSerializer) is False:
            namespace_pk = get_validated_uuid_from_string(
                self.kwargs.get('namespace_pk')
            )
            serializer.namespace_pk = namespace_pk

        return serializer

    def get_queryset(self):
        queryset = super().get_queryset()

        namespace_pk = get_validated_uuid_from_string(
            self.kwargs.get('namespace_pk')
        )

        if namespace_pk:
            queryset = queryset.filter(namespace_id=namespace_pk)
        else:
            queryset = queryset.none()

        return queryset

    def create(self, request, *args, **kwargs):
        namespace_pk = get_validated_uuid_from_string(
            self.kwargs.get('project_pk')
        )
        data = request.data.copy()
        data.update({'namespace': namespace_pk})
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(data)
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED,
                        headers=headers)


class SubscriberViewSet(FieldRequestViewsetMixin, ModelViewSet):
    serializer_class = serializers.SubscriberSerializer
    queryset = \
        serializers.SubscriberSerializer.Meta.model.objects.get_queryset()

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        namespace_pk = get_validated_uuid_from_string(
            request.GET.get('namespace')
        )
        if not namespace_pk:
            content = {'detail': [
                _('Namespace not provided or not valid.'),
            ]}
            return Response(data=content,
                            status=status.HTTP_400_BAD_REQUEST)

        queryset = queryset.filter(namespace_id=namespace_pk)

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)

        if page is not None:
            return self.get_paginated_response(serializer.data)

        return Response(serializer.data)

class DeviceViewSet(FieldRequestViewsetMixin, ModelViewSet):
    serializer_class = serializers.DeviceSerializer
    queryset = serializers.DeviceSerializer.Meta.model.objects.get_queryset()

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class NotificationViewSet(ModelViewSet):
    serializer_class = serializers.NotificationSerializer
    queryset = \
        serializers.NotificationSerializer.Meta.model.objects.get_queryset()

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_serializer(self, *args, **kwargs):
        serializer = super().get_serializer(*args, **kwargs)

        if isinstance(serializer, ListSerializer) is False:
            subscriber_pk = get_validated_uuid_from_string(
                self.kwargs.get('subscriber_pk')
            )
            serializer.subscriber_pk = subscriber_pk

        return serializer

    def get_queryset(self):
        queryset = super().get_queryset()

        subscriber_pk = get_validated_uuid_from_string(
            self.kwargs.get('subscriber_pk')
        )

        if subscriber_pk:
            queryset = queryset.filter(subscriber_id=subscriber_pk)
        else:
            queryset = queryset.none()

        return queryset

    def create(self, request, *args, **kwargs):
        subscriber_pk = get_validated_uuid_from_string(
            self.kwargs.get('project_pk')
        )
        data = request.data.copy()
        data.update({'subscriber': device_pk})
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(data)
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED,
                        headers=headers)

class BaseTransmissionViewSet(ReadOnlyModelViewSet):
    serializer_class = serializers.TransmissionSerializer
    queryset = \
        serializers.TransmissionSerializer.Meta.model.objects.get_queryset()

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class DeviceTransmissionViewSet(BaseTransmissionViewSet):

    def get_queryset(self):
        queryset = super().get_queryset()

        device_pk = get_validated_uuid_from_string(
            self.kwargs.get('device_pk')
        )

        if device_pk:
            queryset = queryset.filter(device_id=device_pk)
        else:
            queryset = queryset.none()

        return queryset

class SubscriberTransmissionViewSet(BaseTransmissionViewSet):
    
    def get_queryset(self):
        queryset = super().get_queryset()

        subscriber_pk = get_validated_uuid_from_string(
            self.kwargs.get('subscriber_pk')
        )

        if subscriber_pk:
            queryset = queryset.filter(device__subscriber_id=subscriber_pk)
        else:
            queryset = queryset.none()

        return queryset