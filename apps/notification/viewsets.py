from rest_framework.viewsets import ModelViewSet

from . import serializers


class NamespaceViewSet(ModelViewSet):
    serializer_class = serializers.NamespaceSerializer
    queryset = \
        serializers.NamespaceSerializer.Meta.model.objects.get_queryset()


class GroupViewSet(ModelViewSet):
    serializer_class = serializers.GroupSerializer
    queryset = serializers.GroupSerializer.Meta.model.objects.get_queryset()


class SubscriberViewSet(ModelViewSet):
    serializer_class = serializers.SubscriberSerializer
    queryset = \
        serializers.SubscriberSerializer.Meta.model.objects.get_queryset()


class DeviceViewSet(ModelViewSet):
    serializer_class = serializers.DeviceSerializer
    queryset = serializers.DeviceSerializer.Meta.model.objects.get_queryset()


class NotificationViewSet(ModelViewSet):
    serializer_class = serializers.NotificationSerializer
    queryset = \
        serializers.NotificationSerializer.Meta.model.objects.get_queryset()
