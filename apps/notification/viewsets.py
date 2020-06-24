from rest_framework.viewsets import ModelViewSet

from .serializers import NamespaceSerializer, GroupSerializer


class NamespaceViewSet(ModelViewSet):
    serializer_class = NamespaceSerializer
    queryset = NamespaceSerializer.Meta.model.objects.get_queryset()

class GroupViewSet(ModelViewSet):
    serializer_class = GroupSerializer
    queryset = GroupSerializer.Meta.model.objects.get_queryset()