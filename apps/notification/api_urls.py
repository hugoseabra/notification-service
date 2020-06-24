from rest_framework import routers

from . import viewsets

router = routers.DefaultRouter()

router.register('namespaces', viewsets.NamespaceViewSet)

urlpatterns = router.urls