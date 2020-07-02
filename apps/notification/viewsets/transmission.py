from rest_framework import permissions, authentication
from rest_framework.viewsets import ReadOnlyModelViewSet

from core.util.uuid import get_validated_uuid_from_string
from .. import serializers


class BaseTransmissionViewSet(ReadOnlyModelViewSet):
    serializer_class = serializers.TransmissionSerializer
    queryset = \
        serializers.TransmissionSerializer.Meta.model.objects.get_queryset()

    authentication_classes = (
        authentication.TokenAuthentication,
        authentication.BasicAuthentication,
        authentication.SessionAuthentication,
    )
    permission_classes = (
        permissions.IsAuthenticated,
    )


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


class NotificationTransmissionViewSet(BaseTransmissionViewSet):
    def get_queryset(self):
        queryset = super().get_queryset()

        notification_pk = get_validated_uuid_from_string(
            self.kwargs.get('notification_pk')
        )

        if notification_pk:
            queryset = queryset.filter(notification_id=notification_pk)
        else:
            queryset = queryset.none()

        return queryset
