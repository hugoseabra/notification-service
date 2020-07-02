from rest_framework import status, permissions, authentication
from rest_framework.response import Response
from rest_framework.serializers import ListSerializer
from rest_framework.viewsets import ModelViewSet

from core.util.uuid import get_validated_uuid_from_string
from core.viewsets import FieldRequestViewsetMixin
from .. import serializers


class GroupViewSet(FieldRequestViewsetMixin, ModelViewSet):
    serializer_class = serializers.GroupSerializer
    queryset = serializers.GroupSerializer.Meta.model.objects.get_queryset()

    authentication_classes = (
        authentication.TokenAuthentication,
        authentication.BasicAuthentication,
        authentication.SessionAuthentication,
    )
    permission_classes = (
        permissions.IsAuthenticated,
    )

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

