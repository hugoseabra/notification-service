from rest_framework.viewsets import ModelViewSet

from .serializers import NamespaceSerializer


class NamespaceViewSet(ModelViewSet):
    serializer_class = NamespaceSerializer
    queryset = NamespaceSerializer.Meta.model.objects.get_queryset()