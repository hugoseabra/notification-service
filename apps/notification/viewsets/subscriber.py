from django.utils.translation import gettext_lazy as _
from rest_framework import status, permissions, authentication
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from core.util.uuid import get_validated_uuid_from_string
from core.viewsets import FieldRequestViewsetMixin
from .. import serializers


class SubscriberViewSet(FieldRequestViewsetMixin, ModelViewSet):
    serializer_class = serializers.SubscriberSerializer
    queryset = \
        serializers.SubscriberSerializer.Meta.model.objects.get_queryset()

    authentication_classes = (
        authentication.TokenAuthentication,
        authentication.BasicAuthentication,
        authentication.SessionAuthentication,
    )
    permission_classes = (
        permissions.IsAuthenticated,
    )

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
