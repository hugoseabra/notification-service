from rest_framework.viewsets import ModelViewSet

from .serializers import NamespaceSerializer, GroupSerializer, SubscriberSerializer


class NamespaceViewSet(ModelViewSet):
    serializer_class = NamespaceSerializer
    queryset = NamespaceSerializer.Meta.model.objects.get_queryset()
    
class GroupViewSet(ModelViewSet):
    serializer_class = GroupSerializer
    queryset = GroupSerializer.Meta.model.objects.get_queryset()

class SubscriberViewSet(ModelViewSet):
    serializer_class = SubscriberSerializer
    queryset = SubscriberSerializer.Meta.model.objects.get_queryset()