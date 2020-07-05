from rest_framework import permissions, authentication
from rest_framework.viewsets import ModelViewSet

from .. import serializers


class NamespaceViewSet(ModelViewSet):
    serializer_class = serializers.NamespaceSerializer
    queryset = \
        serializers.NamespaceSerializer.Meta.model.objects.get_queryset()

    authentication_classes = (
        authentication.TokenAuthentication,
        authentication.BasicAuthentication,
        authentication.SessionAuthentication,
    )
    permission_classes = (
        permissions.IsAdminUser,
    )
